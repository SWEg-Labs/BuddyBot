import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

/**
 * Struttura del modello di messaggio
 * che corrisponde (o mappa) il backend.
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
   * @param quantity numero di messaggi da caricare (es. 50)
   */
  getMessages(quantity: number): Observable<DbMessageModel[]> {
    return this.http.post<DbMessageModel[]>(
      `${this.baseUrl}/api/get_messages`,
      { quantity }
    );
  }

  /**
   * Salva un messaggio nel DB.
   * @param message un oggetto che mappa la tua struttura (MessageBaseModel)
   */
  saveMessage(message: DbMessageModel): Observable<{ status: boolean | string }> {
    return this.http.post<{ status: boolean | string }>(
      `${this.baseUrl}/api/save_message`,
      message
    );
  }
}
