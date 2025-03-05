import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ChatService } from './chat.service';

describe('ChatService', () => {
  let service: ChatService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // ------------------- Unit -------------------
    // Arrange
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ChatService]
    });
    service = TestBed.inject(ChatService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    // Assert: verifica che non siano rimaste richieste pendenti
    httpMock.verify();
  });

  // ------------------- Unit -------------------
  it('should create the ChatService instance successfully', () => {
    // Arrange (già fatto in beforeEach)
    // Act & Assert
    expect(service).toBeTruthy();
  });

  // ------------------- Unit -------------------
  it('should correctly invert isUpdatedSubject when checkFileUpdates() is called', () => {
    // Arrange
    let currentValue!: boolean;
    service.isUpdated$.subscribe(value => (currentValue = value));
    const initialValue = currentValue;

    // Act
    service.checkFileUpdates();

    // Assert
    expect(currentValue).toBe(!initialValue);
  });

  // -------------- Integration -----------------
  it('should call the GET /api/chat/suggestions/initial endpoint and handle the response in getInitialSuggestions()', () => {
    // Arrange
    const mockSuggestions = ['Suggerimento 1', 'Suggerimento 2'];
    let result: string[] = [];

    // Act
    service.getInitialSuggestions().subscribe(res => (result = res));
    const req = httpMock.expectOne('http://localhost:5000/api/chat/suggestions/initial');
    req.flush(mockSuggestions);

    // Assert
    expect(req.request.method).toBe('GET');
    expect(result).toEqual(mockSuggestions);
  });

  // -------------- Integration -----------------
  it('should call the POST /api/chat endpoint in sendMessage() and return the server response', () => {
    // Arrange
    const fakeReply = { response: 'Risposta dal server' };
    let actualReply: string | undefined;

    // Act
    service.sendMessage('Hello').subscribe(res => {
      actualReply = res.response;
    });
    const req = httpMock.expectOne('http://localhost:5000/api/chat');
    req.flush(fakeReply);

    // Assert
    expect(req.request.method).toBe('POST');
    expect(actualReply).toBe('Risposta dal server');
  });
});
