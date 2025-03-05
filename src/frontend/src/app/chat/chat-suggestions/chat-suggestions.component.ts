import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../chat.service';

@Component({
  standalone: true,
  selector: 'app-chat-suggestions',
  templateUrl: './chat-suggestions.component.html',
  styleUrls: ['./chat-suggestions.component.scss'],
  imports: [CommonModule]
})
export class ChatSuggestionsComponent implements OnInit {
  @Input() lastMessageTimestamp!: number;
  @Output() suggestionClicked = new EventEmitter<string>();

  initialSuggestions: string[] = [];
  continuationSuggestions: string[] = [];
  showInitial = true;

  loadError = false;

  constructor(private chatService: ChatService) {}

  ngOnInit() {
    this.checkTime();

    if (!this.showInitial) {
      this.chatService.getContinuationSuggestions().subscribe({
        next: (suggestions) => {
          this.continuationSuggestions = suggestions;
        },
        error: (err) => {
          console.error('Errore nel caricamento dei consigli', err);
          this.loadError = true;
        }
      });
    }
  }

  private checkTime() {
    const now = Date.now();
    const diff = now - this.lastMessageTimestamp;
    const fiveMinutes = 5 * 60 * 1000;
    this.showInitial = diff > fiveMinutes; 
  }

  onSuggestionClick(text: string) {
    console.log('Suggestion clicked:', text);
    this.suggestionClicked.emit(text);
  }
  
}
