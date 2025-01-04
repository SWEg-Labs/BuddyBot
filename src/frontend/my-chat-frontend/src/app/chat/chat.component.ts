import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ChatService } from '../chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  template: `
    <div class="chat-container">
      <div *ngFor="let msg of messages">
        <strong>{{ msg.sender }}:</strong> {{ msg.text }}
      </div>

      <input
        [(ngModel)]="userInput"
        (keyup.enter)="send()"
        placeholder="Digita un messaggio..."
      />
      <button (click)="send()">Invia</button>
      <button (click)="updateJira()">Aggiorna Jira</button>
      <button (click)="updateGithub()">Aggiorna Github</button>
      <button (click)="updateConfluence()">Aggiorna Confluence</button>
    </div>
  `,
  imports: [CommonModule, FormsModule],
  styles: [
    `
      .chat-container {
        max-width: 600px;
        margin: 20px auto;
        padding: 10px;
        border: 1px solid #ccc;
        background-color: #fff;
      }
      input {
        width: 80%;
        padding: 0.5rem;
        margin-right: 0.5rem;
      }
      button {
        padding: 0.5rem 1rem;
        cursor: pointer;
      }
    `,
  ],
})
export class ChatComponent {
  messages: Array<{ sender: string; text: string }> = [];
  userInput: string = '';

  constructor(private chatService: ChatService) {}

  send() {
    const message = this.userInput.trim();
    if (!message) return;

    this.messages.push({ sender: 'Utente', text: message });

    this.chatService.sendMessage(message).subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: res.response });
      },
      error: (err: any) => {
        console.error('Errore nella risposta', err);
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore!' });
      },
    });
    this.userInput = '';
  }


  updateJira() {
    this.chatService.loadJira().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: res.response });
      },
      error: (err: any) => {
        console.error('Errore nella risposta', err);
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore! Caricamento file Jira non riuscito, riprova piu tardi' });
      },
    });
    this.userInput = '';
  }

  updateGithub() {
    this.chatService.loadGithub().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: res.response });
      },
      error: (err: any) => {
        console.error('Errore nella risposta', err);
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore! Caricamento file Github non riuscito, riprova piu tardi' });
      },
    });
    this.userInput = '';
  }

  updateConfluence() {
    this.chatService.loadConfluence().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: res.response });
      },
      error: (err: any) => {
        console.error('Errore nella risposta', err);
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore! Caricamento file Confluence non riuscito, riprova piu tardi' });
      },
    });
    this.userInput = '';
  }
}
