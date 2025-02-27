import { Component, OnInit, ViewChild  } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import { ChatHeaderComponent } from '../chat-header/chat-header.component';
import { ChatMessagesComponent } from '../chat-messages/chat-messages.component';
import { ChatInputComponent } from '../chat-input/chat-input.component';
import { ChatActionsComponent } from '../chat-actions/chat-actions.component';

import { ChatService } from '../chat.service';
import { IMessage } from '../../models/message.model';

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
    ChatInputComponent,
    ChatActionsComponent
  ],
})
export class ChatContainerComponent implements OnInit {
  messages: IMessage[] = [];
  userInput: string = '';
  isLoading: boolean = false;
  showScrollToBottom: boolean = false;
  @ViewChild(ChatMessagesComponent) messagesComponent!: ChatMessagesComponent;


  constructor(private chatService: ChatService) {}

  ngOnInit(): void {
    // Eventuali inizializzazioni
  }

  onScrollChange(isScrolledUp: boolean): void {
    this.showScrollToBottom = isScrolledUp;
  }

  onSendMessage(message: string) {
    const text = message.trim();
    if (!text) return;
  
    this.messages.push({ sender: 'Utente', text });
    this.isLoading = true;
  
    setTimeout(() => this.scrollToBottom(), 0);
  
    this.chatService.sendMessage(text).subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(res.response) });
        this.isLoading = false;
  
        setTimeout(() => this.scrollToBottom(), 0);
      },
      error: (err) => {
        console.error('Errore nella risposta', err);
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore!' });
        this.isLoading = false;
  
        setTimeout(() => this.scrollToBottom(), 0);
      },
    });
  }
  
  


  updateJira() {
    this.isLoading = true;
    this.chatService.loadJira().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(`Jira: ${res.response}`) });
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Errore Jira', err);
        this.messages.push({ sender: 'Bot', text: 'Errore nel caricamento di Jira!' });
        this.isLoading = false;

       // Scrolla al fondo dopo aver ricevuto la risposta
      this.scrollToBottom();
      },
    });
  }

  updateGithub() {
    this.isLoading = true;
    this.chatService.loadGithub().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(`GitHub: ${res.response}`) });
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Errore GitHub', err);
        this.messages.push({ sender: 'Bot', text: 'Errore nel caricamento di GitHub!' });
        this.isLoading = false;

      // Scrolla al fondo dopo aver ricevuto la risposta
      this.scrollToBottom();
      },
    });
  }

  updateConfluence() {
    this.isLoading = true;
    this.chatService.loadConfluence().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(`Confluence: ${res.response}`) });
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Errore Confluence', err);
        this.messages.push({ sender: 'Bot', text: 'Errore nel caricamento di Confluence!' });
        this.isLoading = false;

      // Scrolla al fondo dopo aver ricevuto la risposta
      this.scrollToBottom();
      },
    });
  }

  /**
   * Formattazione generica: grassetto con **testo**, link cliccabili e line break
   */
  private formatResponse(response: string): string {
    return response
      // Titoli: ### Titolo -> <h3>Titolo</h3>
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      // Grassetto: **testo** -> <strong>testo</strong>
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Link in formato cliccabile: http(s):// -> <a href="...">...</a>
      .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>')
      // Newline: \n -> <br>
      .replace(/\n/g, '<br>');
  }
  
  scrollToBottom(): void {
    if (this.messagesComponent) {
      this.messagesComponent.scrollToBottom();
    }
  }  

  
}
