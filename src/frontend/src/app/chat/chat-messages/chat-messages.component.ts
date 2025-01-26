import { Component, Input, AfterViewChecked, ElementRef, ViewChild, Output, EventEmitter  } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IMessage } from '../../models/message.model';
import { ChatLoadingIndicatorComponent } from '../chat-loadind-indicator/chat-loading-indicator.component';

@Component({
  standalone: true,
  selector: 'app-chat-messages',
  templateUrl: './chat-messages.component.html',
  styleUrls: ['./chat-messages.component.scss'],
  imports: [CommonModule, ChatLoadingIndicatorComponent],
})
export class ChatMessagesComponent implements AfterViewChecked {
  @Input() messages: IMessage[] = [];
  @Input() isLoading = false;

  @ViewChild('scrollMe') private readonly messagesContainer!: ElementRef;

  @Output() isScrolledUp = new EventEmitter<boolean>();

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }  

  public scrollToBottom(): void {
    console.log('Scroll to bottom triggered');
    if (this.messagesContainer) {
      const element = this.messagesContainer.nativeElement;
      element.scrollTop = element.scrollHeight;
    } else {
      console.error('messagesContainer is not defined');
    }
  }
  
  
  

  onScroll(): void {
    const element = this.messagesContainer.nativeElement;
    const isAtBottom = element.scrollHeight - element.scrollTop <= element.clientHeight + 10;
    this.isScrolledUp.emit(!isAtBottom);
  }
  
  }
