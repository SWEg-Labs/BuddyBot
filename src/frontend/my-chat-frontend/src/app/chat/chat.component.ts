import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../chat.service';

@Component({
  selector: 'app-chat',
  standalone: true,
  template: `
    <div class="chat-container">
      <div class="messages">
        <div
          *ngFor="let msg of messages"
          class="message"
          [ngClass]="{'user-message': msg.sender === 'Utente', 'bot-message': msg.sender === 'Bot'}"
        >
          <span class="sender">{{ msg.sender }}:</span>
          <span class="text" [innerHTML]="msg.text"></span>
        </div>
      </div>

      <div class="input-area" *ngIf="!isLoading">
        <input
          [(ngModel)]="userInput"
          (keyup.enter)="send()"
          placeholder="Scrivi un messaggio..."
        />
        <button class="primary" (click)="send()">Invia</button>
      </div>

      <div class="actions" *ngIf="!isLoading">
        <button class="action-button jira" (click)="updateJira()">Aggiorna Jira</button>
        <button class="action-button github" (click)="updateGithub()">Aggiorna GitHub</button>
        <button class="action-button confluence" (click)="updateConfluence()">Aggiorna Confluence</button>
      </div>

      <div *ngIf="isLoading" class="loading-indicator">
        <div class="spinner"></div>
        <p>Caricamento in corso...</p>
      </div>
    </div>
  `,
  imports: [CommonModule, FormsModule],
  styles: [
    `
      .chat-container {
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 8px;
        background-color: #f9f9f9;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }

      .messages {
        max-height: 300px;
        overflow-y: auto;
        margin-bottom: 15px;
        padding: 10px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #ffffff;
      }

      .message {
        margin-bottom: 10px;
        padding: 8px;
        border-radius: 6px;
        font-size: 14px;
      }

      .user-message {
        background-color: #e0f7fa;
        text-align: right;
      }

      .bot-message {
        background-color: #fce4ec;
        text-align: left;
      }

      .sender {
        font-weight: bold;
        margin-right: 5px;
      }

      .input-area {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
      }

      input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
      }

      button {
        padding: 10px 15px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
      }

      .primary {
        background-color: #007bff;
        color: white;
      }

      .actions {
        display: flex;
        gap: 10px;
        justify-content: space-between;
      }

      .action-button {
        flex: 1;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        color: white;
        border-radius: 6px;
      }

      .jira {
        background-color: #0052cc;
      }

      .github {
        background-color: #24292e;
      }

      .confluence {
        background-color: #36c5f0;
      }

      .action-button:hover {
        opacity: 0.9;
      }

      .loading-indicator {
        text-align: center;
        font-size: 16px;
        color: #666;
        margin-top: 10px;
      }

      .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #ccc;
        border-top-color: #007bff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto;
      }

      @keyframes spin {
        to {
          transform: rotate(360deg);
        }
      }
    `,
  ],
})
export class ChatComponent {
  /**
   * Lista dei messaggi nella chat.
   */
  messages: Array<{ sender: string; text: string }> = [];

  /**
   * Testo inserito dall'utente.
   */
  userInput: string = '';

  /**
   * Stato del caricamento.
   */
  isLoading: boolean = false;

  constructor(private chatService: ChatService) {}

  /**
   * Invia un messaggio al chatbot e aggiorna la lista dei messaggi.
   */
  send() {
    const message = this.userInput.trim();
    if (!message) return;

    this.messages.push({ sender: 'Utente', text: message });
    this.isLoading = true;

    this.chatService.sendMessage(message).subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(res.response) });
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Errore nella risposta', err);
        this.messages.push({ sender: 'Bot', text: 'C’è stato un errore!' });
        this.isLoading = false;
      },
    });
    this.userInput = '';
  }

  /**
   * Aggiorna i dati da Jira e notifica l'utente con un messaggio.
   */
  updateJira() {
    this.isLoading = true;
    this.chatService.loadJira().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(`Jira: ${res.response}`) });
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Errore Jira', err);
        this.messages.push({ sender: 'Bot', text: 'Errore nel caricamento di Jira!' });
        this.isLoading = false;
      },
    });
  }

  /**
   * Aggiorna i dati da GitHub e notifica l'utente con un messaggio.
   */
  updateGithub() {
    this.isLoading = true;
    this.chatService.loadGithub().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(`GitHub: ${res.response}`) });
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Errore GitHub', err);
        this.messages.push({ sender: 'Bot', text: 'Errore nel caricamento di GitHub!' });
        this.isLoading = false;
      },
    });
  }

  /**
   * Aggiorna i dati da Confluence e notifica l'utente con un messaggio.
   */
  updateConfluence() {
    this.isLoading = true;
    this.chatService.loadConfluence().subscribe({
      next: (res: { response: string }) => {
        this.messages.push({ sender: 'Bot', text: this.formatResponse(`Confluence: ${res.response}`) });
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Errore Confluence', err);
        this.messages.push({ sender: 'Bot', text: 'Errore nel caricamento di Confluence!' });
        this.isLoading = false;
      },
    });
  }

  /**
   * Formatta la risposta sostituendo i ritorni a capo con tag <br>, i link in formato cliccabile, e il testo con ** in grassetto.
   *
   * @param response - La risposta testuale ricevuta dal server.
   * @returns La risposta formattata.
   */
  private formatResponse(response: string): string {
    return response
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold per **testo**
      .replace(/(https?:\/\/\S+)/g, '<a href="$1" target="_blank">$1</a>') // Link cliccabili
      .replace(/\n/g, '<br>'); // Ritorni a capo
  }
}
