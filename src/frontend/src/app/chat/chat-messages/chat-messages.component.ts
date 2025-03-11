import {Component, Input, AfterViewChecked, AfterViewInit, ElementRef, ViewChild, Output, EventEmitter} from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { Message } from '../../models/message.model';
import { ChatLoadingIndicatorComponent } from '../chat-loading-indicator/chat-loading-indicator.component';

@Component({
  standalone: true,
  selector: 'app-chat-messages',
  templateUrl: './chat-messages.component.html',
  styleUrls: ['./chat-messages.component.scss'],
  imports: [CommonModule, MatIconModule, ChatLoadingIndicatorComponent],
})
export class ChatMessagesComponent implements AfterViewChecked, AfterViewInit {
  @Input() messages: Message[] = [];
  @Input() isLoading = false;
  @Output() isScrolledUp = new EventEmitter<boolean>();
  @ViewChild('scrollMe') private messagesContainer!: ElementRef;
  private keepScrollBottom = true;

  ngAfterViewInit(): void {
    const el = this.messagesContainer.nativeElement as HTMLElement;
    el.addEventListener('click', (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (target.classList.contains('copy-snippet-icon')) {
        const preElement = target
          .closest('.code-container')
          ?.querySelector<HTMLElement>('.snippet-content');
        if (preElement) {
          const codeToCopy = preElement.innerText;
          this.copySnippet(codeToCopy, target);
        }
      }
    });
  }
  

  ngAfterViewChecked(): void {
  }

  onScroll(): void {
    if (!this.messagesContainer) return;
    const el = this.messagesContainer.nativeElement;
    const threshold = 50;
    const distanceFromBottom = el.scrollHeight - (el.scrollTop + el.clientHeight);
    this.keepScrollBottom = distanceFromBottom < threshold;
    const isAtBottom = el.scrollHeight - el.scrollTop <= el.clientHeight + 10;
    this.isScrolledUp.emit(!isAtBottom);
  }

  scrollToBottom(): void {
    if (!this.messagesContainer) return;
    const el = this.messagesContainer.nativeElement;
    el.scrollTop = el.scrollHeight;
  }

  copyToClipboard(msg: Message): void {
    const string_text = String(msg.text);
    const textWithLineBreaks = string_text.replace(/<br\s*\/?>/gi, '\n');
    const sanitizedText = this.stripHtml(textWithLineBreaks);
    let plainText = sanitizedText;
    while (plainText.includes('content_copy')) {
      plainText = plainText.replace('content_copy', '');
    }
    plainText = plainText
      .replace('SafeValue must use [property]=binding: ', '')
      .replace(' (see https://g.co/ng/security#xss)', '')
      .replace(/\s{10,}/g, '\n\n\n');
    navigator.clipboard.writeText(plainText).then(() => {
      msg.copied = true;
      setTimeout(() => (msg.copied = false), 1000);
    });
  }

  private copySnippet(code: string, iconElement: HTMLElement): void {
    navigator.clipboard.writeText(code).then(() => {
      iconElement.classList.add('snippet-copied');
      setTimeout(() => {
        iconElement.classList.remove('snippet-copied');
      }, 1000);
    });
  }

  private stripHtml(html: string): string {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    return tempDiv.textContent || tempDiv.innerText || '';
  }
}
