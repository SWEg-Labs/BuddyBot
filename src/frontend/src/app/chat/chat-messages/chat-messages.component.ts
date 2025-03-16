import { Component, Input, AfterViewInit, ElementRef, ViewChild, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { Message, MessageSender } from '../../models/message.model';
import { ChatLoadingIndicatorComponent } from '../chat-loading-indicator/chat-loading-indicator.component';

@Component({
  standalone: true,
  selector: 'app-chat-messages',
  templateUrl: './chat-messages.component.html',
  styleUrls: ['./chat-messages.component.scss'],
  imports: [CommonModule, MatIconModule, ChatLoadingIndicatorComponent],
})
export class ChatMessagesComponent implements AfterViewInit {
  @Input() messages: Message[] = []
  @Input() isLoading = false
  @Input() loadingOlderMessages = false
  @Input() showScrollToBottom = false
  @Output() isScrolledUp = new EventEmitter<boolean>()
  @Output() loadMoreMessages = new EventEmitter<void>()
  @ViewChild('scrollMe') private readonly messagesContainer!: ElementRef
  messageSender = MessageSender
  private keepScrollBottom = true
  private prevScrollHeight = 0
  private scrollPosition = 0

  ngAfterViewInit(): void {
    const el = this.messagesContainer.nativeElement as HTMLElement

    el.addEventListener('click', (event: MouseEvent) => {
      const target = event.target as HTMLElement
      if (target.classList.contains('copy-snippet-icon')) {
        const preElement = target
          .closest('.code-container')
          ?.querySelector<HTMLElement>('.snippet-content')
        if (preElement) {
          const codeToCopy = preElement.innerText
          this.copySnippet(codeToCopy, target)
        }
      }
    })
  }

  onScroll(): void {
    if (!this.messagesContainer) return
    const el = this.messagesContainer.nativeElement
    const threshold = 50
    
    this.scrollPosition = el.scrollTop
    this.prevScrollHeight = el.scrollHeight
    
    const distanceFromBottom = el.scrollHeight - (el.scrollTop + el.clientHeight)
    this.keepScrollBottom = distanceFromBottom < threshold
    const isAtBottom = distanceFromBottom < 10
    this.isScrolledUp.emit(!isAtBottom)
    
    if (el.scrollTop < threshold && this.messages.length > 0) {
      this.loadMoreMessages.emit()
    }
  }

  maintainScrollPosition(): void {
    if (!this.messagesContainer) return
    const el = this.messagesContainer.nativeElement
    
    if (el.scrollHeight > this.prevScrollHeight) {
      const heightDifference = el.scrollHeight - this.prevScrollHeight
      el.scrollTop = this.scrollPosition + heightDifference
    }
  }

  scrollToBottom(): void {
    if (!this.messagesContainer) return
    const el = this.messagesContainer.nativeElement
    el.scrollTop = el.scrollHeight
  }

  copyToClipboard(msg: Message): void {
    const text = msg.sanitizedContent || msg.content
    const stringText = String(text)
    const textWithLineBreaks = stringText.replace(/<br\s*\/?>/gi, '\n')
    const sanitizedText = this.stripHtml(textWithLineBreaks);
    let plainText = sanitizedText;
    while (plainText.includes('content_copy')) {
      plainText = plainText.replace('content_copy', '');
    }
    plainText = plainText
      .replace('SafeValue must use [property]=binding: ', '')
      .replace(' (see https://g.co/ng/security#xss)', '')
      .replace(/\s{10,}/g, '\n\n\n')
    navigator.clipboard.writeText(plainText).then(() => {
      msg.copied = true
      setTimeout(() => (msg.copied = false), 1000)
    })
  }

  private copySnippet(code: string, iconElement: HTMLElement): void {
    navigator.clipboard.writeText(code).then(() => {
      iconElement.classList.add('snippet-copied')
      setTimeout(() => {
        iconElement.classList.remove('snippet-copied')
      }, 1000)
    })
  }

  private stripHtml(html: string): string {
    const tempDiv = document.createElement('div')
    tempDiv.innerHTML = html
    return tempDiv.textContent || tempDiv.innerText || ''
  }
}