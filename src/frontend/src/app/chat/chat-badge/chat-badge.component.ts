import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../chat.service';
import { LastLoadOutcome } from '../../models/LastLoadOutcome.model';

@Component({
  standalone: true,
  selector: 'app-chat-badge',
  templateUrl: './chat-badge.component.html',
  styleUrls: ['./chat-badge.component.scss'],
  imports: [CommonModule],
})
export class ChatBadgeComponent implements OnInit {
  isUpdated = true;

  constructor(private chatService: ChatService) {}

  ngOnInit(): void {
    // Sottoscrizione allo stato dell’ultimo caricamento
    this.chatService.lastLoadOutcome$.subscribe((outcome: LastLoadOutcome | null) => {
      if (outcome) {
        // Se last_load_ok=true => isUpdated=true
        this.isUpdated = outcome.last_load_ok;
      } else {
        // se outcome=null => default “non aggiornato”
        this.isUpdated = false;
      }
    });
  }
}
