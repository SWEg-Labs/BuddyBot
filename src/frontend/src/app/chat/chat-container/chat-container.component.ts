import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';
import { ChatService } from '../chat.service';
import { Message, MessageSender } from '../../models/message.model';
import { ChatHeaderComponent } from '../chat-header/chat-header.component';
import { ChatMessagesComponent } from '../chat-messages/chat-messages.component';
import { ChatSuggestionsComponent } from '../chat-suggestions/chat-suggestions.component';
import { ChatInputComponent } from '../chat-input/chat-input.component';
import { DatabaseService } from '../database.service';

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
  loadingOlderMessages = false;
  showScrollToBottom = false;
  lastUserQuestion = '';
  lastBotAnswer = '';
  hideSuggestions = false;
  errorMessage = '';
  errorTimeout: any = null;
  currentPage = 1;
  messagesPerPage = 50;
  allMessagesLoaded = false;

  @ViewChild(ChatMessagesComponent) messagesComponent!: ChatMessagesComponent;

  constructor(
    private readonly chatService: ChatService,
    private readonly sanitizer: DomSanitizer,
    private readonly databaseService: DatabaseService
  ) {}

  ngOnInit(): void {
    this.loadOldMessages(this.messagesPerPage, 1);
    this.databaseService.loadLastLoadOutcome();
  }

  loadOldMessages(quantity: number, page: number = 1): void {
    if (page === 1) {
      this.isLoading = true;
    } else {
      this.loadingOlderMessages = true;
    }

    this.databaseService.getMessages(quantity, page).subscribe({
      next: (serverMessages: Message[]) => {
        this.clearErrorMessage();
        if (serverMessages.length === 0) {
          this.allMessagesLoaded = true;
          this.isLoading = false;
          this.loadingOlderMessages = false;
          return;
        }

        serverMessages.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());
            const formattedMessages = serverMessages.map((m) => {
            if (m.sender === MessageSender.CHATBOT) {
              const rawFormatted = this.formatResponse(m.content);
              m.sanitizedContent = this.sanitizer.bypassSecurityTrustHtml(rawFormatted);
              m.copied = false;
            }
          return m;
        });
        if (page > 1) {
          this.messages = [...formattedMessages, ...this.messages];
          setTimeout(() => {
            if (this.messagesComponent) {
              this.messagesComponent.maintainScrollPosition();
            }
          }, 0);
        } else {
          this.messages = formattedMessages;
          setTimeout(() => {
            this.scrollToBottom();
          }, 0);
        }

        this.isLoading = false;
        this.loadingOlderMessages = false;
      },
      error: (err) => {
        console.error('Errore nel caricamento dei messaggi dal DB:', err);
        if (this.messages.length === 0 || page === 1) {
          this.showErrorMessage("Errore nel recupero dello storico dei messaggi");
        } else if (page > 1) {
          this.showTemporaryErrorMessage("Errore nel caricamento dei messaggi precedenti. Riprova tra poco.");
        }
        
        this.isLoading = false;
        this.loadingOlderMessages = false;
      }
    });
  }

  showErrorMessage(message: string): void {
    this.errorMessage = message;
  }
  showTemporaryErrorMessage(message: string, duration: number = 5000): void {
    this.errorMessage = message;
    
    if (this.errorTimeout) {
      clearTimeout(this.errorTimeout);
    }
      this.errorTimeout = setTimeout(() => {
      this.clearErrorMessage();
    }, duration);
  }
  
  clearErrorMessage(): void {
    this.errorMessage = '';
    if (this.errorTimeout) {
      clearTimeout(this.errorTimeout);
      this.errorTimeout = null;
    }
  }

  onLoadMoreMessages(): void {
    if (this.loadingOlderMessages || this.allMessagesLoaded || this.isLoading) return;
    
    this.currentPage++;
    this.loadOldMessages(this.messagesPerPage, this.currentPage);
  }

  onScrollChange(isScrolledUp: boolean): void {
    this.showScrollToBottom = isScrolledUp;
  }

  onSendMessage(text: string) {
    const trimmed = text.trim();
    if (!trimmed) return;

    this.hideSuggestions = true;
    this.lastUserQuestion = '';
    this.lastBotAnswer = '';

    const userMsg = new Message(trimmed, new Date(), MessageSender.USER);
    this.messages.push(userMsg);
    this.lastUserQuestion = trimmed;
    this.isLoading = true;

    setTimeout(() => {
      this.scrollToBottom();
    }, 0);

    this.databaseService.saveMessage(userMsg).subscribe({
      next: (response) => {
        console.log('Risultato del salvataggio del messaggio dell\'utente nel database:', response.success);
        console.log('Messaggio di risposta del database:', response.message);
      },
      error: (err) => {
        console.error('Errore durante il salvataggio del messaggio dell\'utente nel database:', err);
      },
    });

    this.chatService.sendMessage(trimmed).subscribe({
      next: (res) => {
        const botMsg = new Message(res.response, new Date(), MessageSender.CHATBOT);
        const rawFormatted = this.formatResponse(botMsg.content);
        botMsg.sanitizedContent = this.sanitizer.bypassSecurityTrustHtml(rawFormatted);
        this.messages.push(botMsg);
        this.lastBotAnswer = res.response;
        this.lastUserQuestion = trimmed;
        this.lastBotAnswer = res.response;

        botMsg.copied = false;
        this.isLoading = false;
        this.clearErrorMessage();

        setTimeout(() => {
          this.scrollToBottom();
        }, 0);

        this.databaseService.saveMessage(botMsg).subscribe({
          next: (response) => {
            console.log('Risultato del salvataggio del messaggio del chatbot nel database:', response.success);
        console.log('Messaggio di risposta del database:', response.message);
          },
          error: (err) => {
            console.error('Errore durante il salvataggio del messaggio del chatbot nel database:', err);
          },
        });

        this.hideSuggestions = false;
      },
      error: () => {
        const errorMsg = new Message("C'è stato un errore!", new Date(), MessageSender.CHATBOT);
        this.messages.push(errorMsg);
        this.databaseService.saveMessage(errorMsg).subscribe();
        this.isLoading = false;
        this.showTemporaryErrorMessage("Errore nell'invio del messaggio. Riprova tra poco.");
        
        setTimeout(() => {
          this.scrollToBottom();
        }, 0);
      }
    });
  }

  onSuggestionClicked(suggestion: string) {
    this.onSendMessage(suggestion);
  }

  formatResponse(response: string): string {
    const codeRegex = /```(\w+)?([\s\S]*?)```/g;
    const linkRegex = /\b((?:(?:https?:\/\/)|(?:www\.))[\w\-]+(?:\.[\w\-]+)+(?:\/[\w.,@?^=%&:\/~+#\-]*)?)(?=[\s.,;:!?)\]]|$)/gi;
    let formatted = response.replace(codeRegex, (match, maybeLang, codeBlock) => {
      const trimmed = codeBlock.replace(/^\n+|\n+$/g, '');
      const escapedCode = trimmed.replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `
        <div class="code-container">
          <mat-icon title="Copia il codice" class="mat-icon notranslate material-icons mat-ligature-font mat-icon-no-color copy-snippet-icon" aria-hidden="true" data-mat-icon-type="font">content_copy</mat-icon>
          <pre class="snippet-content">${escapedCode}</pre>
        </div>`;
    });
    formatted = formatted
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(linkRegex, '<a href="$1" target="_blank">$1</a>')
      .replace(/\n/g, '<br>');

      const linkBlockRegex = /(Link (?:correlati|utili):(?:<br>.*?))(?=<br><br>|$)/gis;
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