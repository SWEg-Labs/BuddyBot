import { SafeHtml } from '@angular/platform-browser';

export enum MessageSender {
  USER = 'User',
  CHATBOT = 'Chatbot',
}

export class Message {
  public copied?: boolean
  public sanitizedContent?: SafeHtml

  constructor(
    public content: string,
    public timestamp: Date,
    public sender: MessageSender
  ) {}
}
