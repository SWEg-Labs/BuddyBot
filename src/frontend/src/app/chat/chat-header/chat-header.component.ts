import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatBadgeComponent } from '../chat-badge/chat-badge.component';

@Component({
  standalone: true,
  selector: 'app-chat-header',
  templateUrl: './chat-header.component.html',
  styleUrls: ['./chat-header.component.scss'],
  imports: [CommonModule, ChatBadgeComponent],
})
export class ChatHeaderComponent {}
