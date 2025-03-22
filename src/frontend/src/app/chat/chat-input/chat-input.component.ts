import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-chat-input',
  templateUrl: './chat-input.component.html',
  styleUrls: ['./chat-input.component.scss'],
  imports: [CommonModule, FormsModule],
})
export class ChatInputComponent {
  @Input() isLoading = false;
  @Output() sendMessage = new EventEmitter<string>();

  userInput = '';

  onSend() {
    console.log('onSend triggered', this.userInput, this.isLoading);
    if (!this.userInput.trim() || this.isLoading) {
      return;
    }
    this.sendMessage.emit(this.userInput.trim());
    this.userInput = '';
  }
}
