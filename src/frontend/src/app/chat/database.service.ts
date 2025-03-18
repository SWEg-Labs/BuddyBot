import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, BehaviorSubject } from 'rxjs';
import { Message, MessageSender } from '../models/message.model';
import { LastLoadOutcome } from '../models/badge.model';


@Injectable({
  providedIn: 'root',
})
export class DatabaseService {
  private readonly apiBaseUrl = 'http://localhost:5000';

  private readonly lastLoadOutcomeSubject = new BehaviorSubject<LastLoadOutcome>(LastLoadOutcome.TRUE);
  public lastLoadOutcome$ = this.lastLoadOutcomeSubject.asObservable();

  constructor(private readonly http: HttpClient) {}

  getMessages(quantity: number, page: number = 1): Observable<Message[]> {
    return this.http
      .post<any[]>(`${this.apiBaseUrl}/api/get_messages`, { quantity, page })
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

  saveMessage(msg: Message): Observable<{ success: boolean; message: string }> {
    const payload = {
      content: msg.content,
      sender: msg.sender,
      timestamp: msg.timestamp,
    };
    return this.http.post<{ success: boolean; message: string }>(
      `${this.apiBaseUrl}/api/save_message`,
      payload
    );
  }

  loadLastLoadOutcome(): void {
    this.http.post<string>(`${this.apiBaseUrl}/api/get_last_load_outcome`, {})
      .subscribe({
        next: (data) => {
          console.log(data);
          if (data === "True") {
            this.lastLoadOutcomeSubject.next(LastLoadOutcome.TRUE);
          } else if (data === "False") {
            this.lastLoadOutcomeSubject.next(LastLoadOutcome.FALSE);
          } else {
            this.lastLoadOutcomeSubject.next(LastLoadOutcome.ERROR);
          }
        },
        error: (err) => {
          console.error('Errore nel recupero di get_last_load_outcome:', err);
          this.lastLoadOutcomeSubject.next(LastLoadOutcome.ERROR);
        }
      });
  }
}