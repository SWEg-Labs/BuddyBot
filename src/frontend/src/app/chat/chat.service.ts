import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root', 
})
export class ChatService {
  private apiUrl = 'http://localhost:5000/api/chat';


  private isUpdatedSubject = new BehaviorSubject<boolean>(true);
  public isUpdated$ = this.isUpdatedSubject.asObservable();
  private apiBaseUrl = 'http://localhost:5000'; 

  private lastMessageTimestamp: number = Date.now();

  constructor(private http: HttpClient) {}

  checkFileUpdates(): void {
    this.isUpdatedSubject.next(!this.isUpdatedSubject.value);
  }

  getLastMessageTimestamp(): number {
    return this.lastMessageTimestamp;
  }
  setLastMessageTimestamp(time: number) {
    this.lastMessageTimestamp = time;
  }

  sendMessage(message: string): Observable<{ response: string }> {
    this.setLastMessageTimestamp(Date.now());
    return this.http.post<{ response: string }>(this.apiUrl, { message });
  }

  getInitialSuggestions(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiBaseUrl}/api/chat/suggestions/initial`);
  }

  getContinuationSuggestions(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiBaseUrl}/api/chat/suggestions/continuation`);
  }
}
