import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

import { ChatService } from '../chat.service';
import { Message } from '../../models/message.model';
import { ChatHeaderComponent } from '../chat-header/chat-header.component';
import { ChatMessagesComponent } from '../chat-messages/chat-messages.component';
import { ChatSuggestionsComponent } from '../chat-suggestions/chat-suggestions.component';
import { ChatInputComponent } from '../chat-input/chat-input.component';
import { DatabaseService, DbMessageModel } from '../database.service';

@Component({
  standalone: true,
  selector: 'app-chat-container',
  templateUrl: './chat-container.component.html',
  styleUrls: ['./chat-container.component.scss'],
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    ChatHeaderComponent,
    ChatMessagesComponent,
    ChatSuggestionsComponent,
    ChatInputComponent,
  ]
})
export class ChatContainerComponent implements OnInit {
  messages: Message[] = [];
  isLoading = false;
  showScrollToBottom = false;

  @ViewChild(ChatMessagesComponent) messagesComponent!: ChatMessagesComponent;

  constructor(
    private readonly chatService: ChatService,
    private readonly sanitizer: DomSanitizer,
    private databaseService: DatabaseService
  ) {}

  ngOnInit(): void {
    this.loadOldMessages(50);
  }

  private loadOldMessages(quantity: number) {
    this.databaseService.getMessages(quantity).subscribe({
      next: (dbMessages: DbMessageModel[]) => {
        this.messages = dbMessages.map((dbMsg) => {
          const rawFormatted = this.formatResponse(dbMsg.message);
          const sanitized = this.sanitizer.bypassSecurityTrustHtml(rawFormatted);
          return {
            sender: dbMsg.sender,
            text: sanitized,
            copied: false
          };
        });
        this.scrollToBottom();
      },
      error: (err) => {
        console.error('Errore nel caricamento dei messaggi dal DB:', err);
      }
    });
  }

  get lastMessageTime(): number {
    return this.chatService.getLastMessageTimestamp();
  }

  onScrollChange(isScrolledUp: boolean): void {
    this.showScrollToBottom = isScrolledUp;
  }

  onSendMessage(message: string) {
    const text = message.trim();
    if (!text) return;
  
    // 1. Visualizzo immediatamente a schermo il messaggio dell'utente
    this.messages.push({ sender: 'Utente', text });
    this.messagesComponent.scrollToBottom();
  
    // 2. Salvo il messaggio dell'utente su DB
    const userMsg = { message: text, sender: 'Utente' };
    this.databaseService.saveMessage(userMsg).subscribe({
      next: (resp) => {
        console.log('Messaggio utente salvato correttamente', resp);
      },
      error: (err) => {
        console.error('Errore nel salvataggio del messaggio utente:', err);
      },
    });
  
    // 3. Chiedo la risposta al bot
    this.isLoading = true;
    this.chatService.sendMessage(text).subscribe({
      next: (res) => {
        // 4. Aggiungo la risposta bot all'array messages
        const rawFormatted = this.formatResponse(res.response);
        const sanitized = this.sanitizer.bypassSecurityTrustHtml(rawFormatted);
        this.messages.push({ sender: 'Bot', text: sanitized });
  
        // 5. Salvo anche il messaggio del bot nel DB
        const botMsg = { message: res.response, sender: 'Bot' };
        this.databaseService.saveMessage(botMsg).subscribe({
          next: (resp) => {
            console.log('Messaggio bot salvato correttamente', resp);
          },
          error: (err) => {
            console.error('Errore nel salvataggio del messaggio bot:', err);
          },
        });
  
        this.isLoading = false;
        this.messagesComponent.scrollToBottom();
      },
      error: () => {
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore!' });
        this.isLoading = false;
        this.messagesComponent.scrollToBottom();
      },
    });
  }

  onSuggestionClicked(suggestion: string) {
    this.onSendMessage(suggestion);
  }

  private formatResponse(response: string): string {
    const codeRegex = /```(\w+)?([\s\S]*?)```/g;
    let formatted = response.replace(codeRegex, (match, maybeLang, codeBlock) => {
      const trimmed = codeBlock.replace(/^\n+|\n+$/g, '');
      const escapedCode = trimmed
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      return `
        <div class="code-container">
          <mat-icon 
            _ngcontent-ng-c4071621763 
            title="Copia il codice" 
            class="mat-icon notranslate material-icons mat-ligature-font mat-icon-no-color copy-snippet-icon" 
            aria-hidden="true" 
            data-mat-icon-type="font"
          >
            content_copy
          </mat-icon>
          <pre class="snippet-content">${escapedCode}</pre>
        </div>
      `;
    });
  
    formatted = formatted
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>')
      .replace(/\n/g, '<br>');
  
    return formatted;
  }

  scrollToBottom(): void {
    if (this.messagesComponent) {
      this.messagesComponent.scrollToBottom();
    }
  }
}
