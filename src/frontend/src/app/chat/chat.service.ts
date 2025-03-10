import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';

@Injectable({
  providedIn: 'root', 
})
export class ChatService {
  private isUpdatedSubject = new BehaviorSubject<boolean>(true);
  public isUpdated$ = this.isUpdatedSubject.asObservable();
  private apiBaseUrl = 'http://localhost:5000';


  private lastMessageTimestamp: number = Date.now();

  private lastLoadOutcomeSubject = new BehaviorSubject<boolean | null>(null);
  public lastLoadOutcome$ = this.lastLoadOutcomeSubject.asObservable();


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
    return this.http.post<{ response: string }>(`${this.apiBaseUrl}/api/chat`, { message });
  }

  getContinuationSuggestions(payload: {
    question: string;
    answer: string;
    quantity: number;
  }): Observable<Record<string, string>> {
    console.log('Chiamata getContinuationSuggestions(), payload =', payload);

    return this.http
      .post<Record<string, string>>(
        `${this.apiBaseUrl}/api/get_next_possible_questions`,
        payload
      )
      .pipe(
        tap((response) => {
          console.log('Risposta da getContinuationSuggestions():', response);
        }),
        catchError((error) => {
          console.error('Errore da getContinuationSuggestions():', error);
          return throwError(() => error);
        })
      );
  }

  loadLastLoadOutcome(): void {
    this.http.post<boolean>(`${this.apiBaseUrl}/api/get_last_load_outcome`, {})
      .subscribe({
        next: (data) => {
          this.lastLoadOutcomeSubject.next(data);
          console.log("lastOutcome: ", data);
        },
        error: (err) => {
          console.error('Errore nel recupero di get_last_load_outcome:', err);
          this.lastLoadOutcomeSubject.next(false);
        }
      });
  }
}
