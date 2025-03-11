import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { Message, MessageSender } from '../models/message.model';

@Injectable({
  providedIn: 'root',
})
export class DatabaseService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  getMessages(quantity: number): Observable<Message[]> {
    return this.http
      .post<any[]>(`${this.baseUrl}/api/get_messages`, { quantity })
      .pipe(
        map((responseArray: any[]) => {
          return responseArray.map(obj => {
            console.log(obj);
            const dateObj = new Date(obj.timestamp)
            const senderEnum = obj.sender === 'USER' ? MessageSender.USER : MessageSender.CHATBOT
            return new Message(obj.content, dateObj, senderEnum)
          })
        })
      )
  }

  saveMessage(msg: Message): Observable<{ status: boolean | string }> {
    const payload = {
      content: msg.content,
      sender: msg.sender,
      timestamp: msg.timestamp,
    }
    return this.http.post<{ status: boolean | string }>(
      `${this.baseUrl}/api/save_message`,
      payload
    )
  }
}
