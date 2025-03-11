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
  messages: Message[] = []
  isLoading = false
  showScrollToBottom = false
  lastUserQuestion = ''
  lastBotAnswer = ''

  @ViewChild(ChatMessagesComponent) messagesComponent!: ChatMessagesComponent

  constructor(
    private readonly chatService: ChatService,
    private readonly sanitizer: DomSanitizer,
    private readonly databaseService: DatabaseService
  ) {}

  ngOnInit(): void {
    this.loadOldMessages(50)
    this.chatService.loadLastLoadOutcome()
  }

  loadOldMessages(quantity: number) {
    this.databaseService.getMessages(quantity).subscribe({
      next: (serverMessages: Message[]) => {
        serverMessages.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime())
        this.messages = serverMessages.map(m => {
          const rawFormatted = this.formatResponse(m.content)
          m.sanitizedContent = this.sanitizer.bypassSecurityTrustHtml(rawFormatted)
          m.copied = false
          return m
        })
        this.scrollToBottom()
      },
      error: err => {
        console.error('Errore nel caricamento dei messaggi dal DB:', err)
      }
    })
  }

  onScrollChange(isScrolledUp: boolean): void {
    this.showScrollToBottom = isScrolledUp
  }

  onSendMessage(text: string) {
    const trimmed = text.trim()
    if (!trimmed) return
    const userMsg = new Message(trimmed, new Date(), MessageSender.USER)
    this.messages.push(userMsg)
    this.lastUserQuestion = trimmed
    this.isLoading = true
    this.databaseService.saveMessage(userMsg).subscribe()
    this.chatService.sendMessage(trimmed).subscribe({
      next: res => {
        const botMsg = new Message(res.response, new Date(), MessageSender.CHATBOT)
        const rawFormatted = this.formatResponse(botMsg.content)
        botMsg.sanitizedContent = this.sanitizer.bypassSecurityTrustHtml(rawFormatted)
        botMsg.copied = false
        this.messages.push(botMsg)
        this.lastBotAnswer = res.response
        this.databaseService.saveMessage(botMsg).subscribe()
        this.isLoading = false
        this.scrollToBottom()
      },
      error: () => {
        const errorMsg = new Message('C’è stato un errore!', new Date(), MessageSender.CHATBOT)
        this.messages.push(errorMsg)
        this.databaseService.saveMessage(errorMsg).subscribe()
        this.isLoading = false
        this.scrollToBottom()
      }
    })
    this.scrollToBottom()
  }

  onSuggestionClicked(suggestion: string) {
    this.onSendMessage(suggestion)
  }

  formatResponse(response: string): string {
    const codeRegex = /```(\w+)?([\s\S]*?)```/g
    let formatted = response.replace(codeRegex, (match, maybeLang, codeBlock) => {
      const trimmed = codeBlock.replace(/^\n+|\n+$/g, '')
      const escapedCode = trimmed
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
      return `
        <div class="code-container">
          <mat-icon title="Copia il codice" class="mat-icon notranslate material-icons mat-ligature-font mat-icon-no-color copy-snippet-icon" aria-hidden="true" data-mat-icon-type="font">content_copy</mat-icon>
          <pre class="snippet-content">${escapedCode}</pre>
        </div>`
    })
    formatted = formatted
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>')
      .replace(/\n/g, '<br>')
    const linkBlockRegex = /(Link correlati:(?:<br>.*?))(?=<br><br>|$)/gs
    formatted = formatted.replace(linkBlockRegex, fullMatch => {
      const clean = fullMatch.replace(/<br>$/, '')
      return `<div class="related-links-block">${clean}</div>`
    })
    return formatted
  }

  scrollToBottom(): void {
    if (this.messagesComponent) {
      this.messagesComponent.scrollToBottom()
    }
  }
}
