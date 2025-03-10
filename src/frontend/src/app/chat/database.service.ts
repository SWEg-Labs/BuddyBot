import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';

/**
 * Struttura del modello di messaggio
 */
export interface DbMessageModel {
  content: string;
  sender: string;
  timestamp: Date;
}

@Injectable({
  providedIn: 'root',
})
export class DatabaseService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  /**
   * Recupera un certo numero di messaggi dal DB.
   */
  getMessages(quantity: number): Observable<DbMessageModel[]> {
    console.log('Richiesta getMessages, payload =', { quantity });
    
    return this.http
      .post<DbMessageModel[]>(`${this.baseUrl}/api/get_messages`, { quantity })
      .pipe(
        tap((response) => {
          console.log('Risposta da getMessages:', response);
        }),
        catchError((error) => {
          console.error('Errore da getMessages:', error);
          return throwError(() => error);
        })
      );
  }

  /**
   * Salva un messaggio nel DB.
   */
  saveMessage(message: DbMessageModel): Observable<{ status: boolean | string }> {
    console.log('Richiesta saveMessage, payload =', message);
    
    return this.http
      .post<{ status: boolean | string }>(
        `${this.baseUrl}/api/save_message`,
        message
      )
      .pipe(
        tap((resp) => {
          console.log('Risposta da saveMessage:', resp);
        }),
        catchError((error) => {
          console.error('Errore da saveMessage:', error);
          return throwError(() => error);
        })
      );
  }
}
