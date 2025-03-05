import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../chat.service';

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
    this.chatService.isUpdated$.subscribe(value => {
      this.isUpdated = value;
    });
  }

  onToggleStatus() {
    this.chatService.checkFileUpdates();
  }
}
