import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../chat.service';
import { LastLoadOutcome } from '../../models/badge.model';

@Component({
  standalone: true,
  selector: 'app-chat-badge',
  templateUrl: './chat-badge.component.html',
  styleUrls: ['./chat-badge.component.scss'],
  imports: [CommonModule],
})
export class ChatBadgeComponent implements OnInit {
  lastLoadOutcome: LastLoadOutcome = LastLoadOutcome.TRUE
  public LastLoadOutcome = LastLoadOutcome

  constructor(private readonly chatService: ChatService) {}

  ngOnInit(): void {
    this.chatService.lastLoadOutcome$.subscribe({
      next: (outcome: LastLoadOutcome) => {
        this.lastLoadOutcome = outcome
      }
    })
  }

  onToggleStatus(): void {
    this.chatService.checkFileUpdates()
  }

  get isUpdated(): boolean {
    return this.lastLoadOutcome === LastLoadOutcome.TRUE
  }
}
