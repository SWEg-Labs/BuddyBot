import { Component, Input, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../chat.service';

@Component({
  standalone: true,
  selector: 'app-chat-suggestions',
  templateUrl: './chat-suggestions.component.html',
  styleUrls: ['./chat-suggestions.component.scss'],
  imports: [CommonModule]
})
export class ChatSuggestionsComponent implements OnChanges {
  @Input() question: string = '';
  @Input() answer: string = '';
  @Output() suggestionClicked = new EventEmitter<string>();

  continuationSuggestions: string[] = [];
  loadError = false;

  constructor(private chatService: ChatService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if ((changes['question'] || changes['answer']) && this.canLoadSuggestions()) {
      this.getContinuationSuggestions();
    }
  }

  private canLoadSuggestions(): boolean {
    return this.question.trim().length > 0 && this.answer.trim().length > 0;
  }

  private getContinuationSuggestions() {
    const payload = {
      question: this.question,
      answer: this.answer,
      quantity: 5
    };
    this.chatService.getContinuationSuggestions(payload).subscribe({
      next: (res) => {
        this.continuationSuggestions = Object.values(res);
      },
      error: (err) => {
        console.error('Errore nel caricamento delle suggestions', err);
        this.loadError = true;
      }
    });
  }

  onSuggestionClick(text: string) {
    this.suggestionClicked.emit(text);
  }
}
