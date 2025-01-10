import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private apiUrl = 'http://localhost:5000/api/chat';
  private apiLoadJira = 'http://localhost:5000/api/jira/load';
  private apiloadGithub = 'http://localhost:5000/api/github/load';
  private apiLoadConfluence = 'http://localhost:5000/api/confluence/load';

  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<{ response: string }> {
    return this.http.post<{ response: string }>(this.apiUrl, { message });
  }

  loadJira(): Observable<{ response: string }> {
    return this.http.get<{ response: string }>(this.apiLoadJira, {});
  }

  loadGithub(): Observable<{ response: string }> {
    return this.http.get<{ response: string }>(this.apiloadGithub, {});
  }

  loadConfluence(): Observable<{ response: string }> {
    return this.http.get<{ response: string }>(this.apiLoadConfluence, {});
  }
}
