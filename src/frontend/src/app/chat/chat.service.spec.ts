import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ChatService } from './chat.service';

describe('ChatService', () => {
  let service: ChatService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // Test di Unità
    // Prepara
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ChatService]
    });

    service = TestBed.inject(ChatService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  // Test di Unità
  it('deve creare correttamente l’istanza di ChatService', () => {
    // Esegui e Verifica
    expect(service).toBeTruthy();
  });

  // Test di Unità
  it('deve invertire correttamente isUpdatedSubject quando viene chiamato checkFileUpdates()', () => {
    // Prepara
    let currentValue!: boolean;
    service.isUpdated$.subscribe(value => (currentValue = value));
    const valoreIniziale = currentValue;

    // Esegui
    service.checkFileUpdates();

    // Verifica
    expect(currentValue).toBe(!valoreIniziale);
  });

  // Test di Unità
  it('deve restituire il valore corretto di lastMessageTimestamp', () => {
    // Prepara
    const now = Date.now();

    // Esegui
    service.setLastMessageTimestamp(now);

    // Verifica
    expect(service.getLastMessageTimestamp()).toBe(now);
  });

  // Test di Integrazione
  it('deve chiamare l’endpoint GET /api/chat/suggestions/initial e gestire la risposta in getInitialSuggestions()', () => {
    const mockSuggestions = ['Suggerimento 1', 'Suggerimento 2'];
    let result: string[] = [];
    service.getInitialSuggestions().subscribe(res => (result = res));
    const req = httpMock.expectOne('http://localhost:5000/api/chat/suggestions/initial');
    req.flush(mockSuggestions);
    expect(req.request.method).toBe('GET');
    expect(result).toEqual(mockSuggestions);
  });

  // Test di Integrazione
  it('deve chiamare l’endpoint GET /api/chat/suggestions/continuation e gestire la risposta in getContinuationSuggestions()', () => {
    const mockSuggestions = ['Cont1', 'Cont2'];
    let result: string[] = [];
    service.getContinuationSuggestions().subscribe(res => (result = res));
    const req = httpMock.expectOne('http://localhost:5000/api/chat/suggestions/continuation');
    req.flush(mockSuggestions);
    expect(req.request.method).toBe('GET');
    expect(result).toEqual(mockSuggestions);
  });

  // Test di Integrazione
  it('deve chiamare l’endpoint POST /api/chat in sendMessage() e restituire la risposta del server', () => {
    const fakeReply = { response: 'Risposta dal server' };
    let actualReply: string | undefined;
    service.sendMessage('Hello').subscribe(res => {
      actualReply = res.response;
    });
    const req = httpMock.expectOne('http://localhost:5000/api/chat');
    req.flush(fakeReply);
    expect(req.request.method).toBe('POST');
    expect(actualReply).toBe('Risposta dal server');
  });
});
