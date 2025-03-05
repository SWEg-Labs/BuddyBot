import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { DomSanitizer} from '@angular/platform-browser';
import { ChatService } from '../chat.service';
import { Message } from '../../models/message.model';
import { ChatHeaderComponent } from '../chat-header/chat-header.component';
import { ChatMessagesComponent } from '../chat-messages/chat-messages.component';
import { ChatSuggestionsComponent } from '../chat-suggestions/chat-suggestions.component';
import { ChatInputComponent } from '../chat-input/chat-input.component';
import DOMPurify from 'dompurify';

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

  constructor(private chatService: ChatService, private sanitizer: DomSanitizer) {}

  ngOnInit(): void {}

  get lastMessageTime(): number {
    return this.chatService.getLastMessageTimestamp();
  }

  onScrollChange(isScrolledUp: boolean): void {
    this.showScrollToBottom = isScrolledUp;
  }

  onSendMessage(message: string) {
    const text = message.trim();
    if (!text) return;
    this.messages.push({ sender: 'Utente', text });
    this.messagesComponent.scrollToBottom();
  
    this.isLoading = true;
    this.chatService.sendMessage(text).subscribe({
      next: (res) => {
        const rawFormatted = this.formatResponse(res.response);
        const sanitized = this.sanitizer.bypassSecurityTrustHtml(rawFormatted);
        this.messages.push({ sender: 'Bot', text: sanitized });
        this.isLoading = false;
        this.messagesComponent.scrollToBottom();
      },
      error: () => {
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore!' });
        this.isLoading = false;
        this.messagesComponent.scrollToBottom();
      }
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
