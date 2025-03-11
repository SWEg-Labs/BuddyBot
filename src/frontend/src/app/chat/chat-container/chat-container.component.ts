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
  lastUserQuestion = '';
  lastBotAnswer = '';

  @ViewChild(ChatMessagesComponent) messagesComponent!: ChatMessagesComponent;

  constructor(
    private readonly chatService: ChatService,
    private readonly sanitizer: DomSanitizer,
    private readonly databaseService: DatabaseService
  ) {}

  ngOnInit(): void {
    this.loadOldMessages(50);
    this.chatService.loadLastLoadOutcome();
  }

  private loadOldMessages(quantity: number) {
    this.databaseService.getMessages(quantity).subscribe({
      next: (dbMessages: DbMessageModel[]) => {
        dbMessages.sort((a, b) => {
          return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
        });
          this.messages = dbMessages.map((dbMsg) => {
          let mappedSender: string;
          if (dbMsg.sender === 'USER') {
            mappedSender = 'Utente';
          } else if (dbMsg.sender === 'CHATBOT') {
            mappedSender = 'Bot';
          } else {
            mappedSender = 'Utente';
          }
          const rawFormatted = this.formatResponse(dbMsg.content);
          const sanitized = this.sanitizer.bypassSecurityTrustHtml(rawFormatted);
            return {
            sender: mappedSender, 
            text: sanitized,
            copied: false,
          };
        });
  
        this.scrollToBottom();
      },
      error: (err) => {
        console.error('Errore nel caricamento dei messaggi dal DB:', err);
      }
    });
  }
  

  onScrollChange(isScrolledUp: boolean): void {
    this.showScrollToBottom = isScrolledUp;
  }

  onSendMessage(message: string) {
    const text = message.trim();
    if (!text) return;
  
    this.messages.push({ sender: 'Utente', text });
    this.messagesComponent.scrollToBottom();
  
    this.lastUserQuestion = text;
    const userMsg = { 
      content: text, 
      sender: 'USER',
      timestamp: new Date()
    };
  
    console.log('Stiamo inviando:', text);
    console.log('lastUserQuestion =', this.lastUserQuestion);
  
    this.databaseService.saveMessage(userMsg).subscribe({
      next: (resp) => {
        console.log('Messaggio utente salvato correttamente', resp);
      },
      error: (err) => {
        console.error('Errore nel salvataggio del messaggio utente:', err);
      },
    });

    this.isLoading = true;

    this.chatService.sendMessage(text).subscribe({
      next: (res) => {
        const rawFormatted = this.formatResponse(res.response);
        const sanitized = this.sanitizer.bypassSecurityTrustHtml(rawFormatted);
        this.messages.push({ sender: 'Bot', text: sanitized });
        console.log('Risposta dal server:', res.response);
        this.lastBotAnswer = res.response;
  
        const botMsg = { 
          content: res.response, 
          sender: 'CHATBOT',
          timestamp: new Date()
        };
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
  
        const botMsg = {
          content: 'C’è stato un errore!',
          sender: 'CHATBOT',
          timestamp: new Date()
        };
        this.databaseService.saveMessage(botMsg).subscribe({
          next: (resp) => {
            console.log('Messaggio di errore del bot salvato correttamente', resp);
          },
          error: (err) => {
            console.error('Errore nel salvataggio del messaggio di errore del bot:', err);
          },
        });
  
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
          <mat-icon _ngcontent-ng-c4071621763 title="Copia il codice" class="mat-icon notranslate material-icons mat-ligature-font mat-icon-no-color copy-snippet-icon" aria-hidden="true" data-mat-icon-type="font">content_copy</mat-icon>
          <pre class="snippet-content">${escapedCode}</pre>
        </div>`;
    });

    formatted = formatted
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>')
      .replace(/\n/g, '<br>');

    const linkBlockRegex = /(Link correlati:(?:<br>.*?))(?=<br><br>|$)/gs;
    formatted = formatted.replace(linkBlockRegex, (fullMatch) => {
      const clean = fullMatch.replace(/<br>$/, '');
      return `<div class="related-links-block">${clean}</div>`;
    });

    return formatted;
  }

  scrollToBottom(): void {
    if (this.messagesComponent) {
      this.messagesComponent.scrollToBottom();
    }
  }
}
