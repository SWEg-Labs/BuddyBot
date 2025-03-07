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
  it('Verifica che venga creata correttamente un’istanza di ChatService', () => {
    // Assert
    expect(service).toBeTruthy();
  });

  // Test di Unità
  it('Verifica che, alla chiamata del metodo checkFileUpdates di ChatService, venga invertita correttamente la variabile '+
    'booleana isUpdatedSubject', () => {
    // Arrange
    let currentValue!: boolean;
    service.isUpdated$.subscribe(value => (currentValue = value));
    const valoreIniziale = currentValue;

    // Act
    service.checkFileUpdates();

    // Assert
    expect(currentValue).toBe(!valoreIniziale);
  });

  // Test di Unità
  it('Verifica che ChatService restituisca il valore corretto di lastMessageTimestamp', () => {
    // Arrange
    const now = Date.now();

    // Act
    service.setLastMessageTimestamp(now);

    // Assert
    expect(service.getLastMessageTimestamp()).toBe(now);
  });


  // DA RIMUOVERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  // Test di Integrazione
  it('Verifica il metodo getInitialSuggestions di ChatService chiami l’endpoint GET /api/chat/suggestions/initial '+
    'e ne gestisca la risposta', () => {
    // Arrange
    const mockSuggestions = ['Suggerimento 1', 'Suggerimento 2'];
    let result: string[] = [];
    service.getInitialSuggestions().subscribe(res => (result = res));
    const req = httpMock.expectOne('http://localhost:5000/api/chat/suggestions/initial');

    // Act
    req.flush(mockSuggestions);

    // Assert
    expect(req.request.method).toBe('GET');
    expect(result).toEqual(mockSuggestions);
  });
  

  // Test di Integrazione
  it('Verifica il metodo getContinuationSuggestions di ChatService chiami l’endpoint GET /api/chat/suggestions/continuation '+
    'e ne gestisca la risposta', () => {
    // Arrange
    const mockSuggestions = ['Cont1', 'Cont2'];
    let result: string[] = [];
    service.getContinuationSuggestions().subscribe(res => (result = res));
    const req = httpMock.expectOne('http://localhost:5000/api/chat/suggestions/continuation');

    // Act
    req.flush(mockSuggestions);

    // Assert
    expect(req.request.method).toBe('GET');
    expect(result).toEqual(mockSuggestions);
  });

  // Test di Integrazione
  it('Verifica il metodo sendMessage di ChatService chiami l’endpoint POST /api/chat e ne gestisca la risposta', () => {
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
