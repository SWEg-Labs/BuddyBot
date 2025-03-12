import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ChatService } from './chat.service';

// Test di Unità e Integrazione
import { of } from 'rxjs';

describe('ChatService', () => {
  let service: ChatService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // Arrange
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

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================

  it('Dovrebbe creare correttamente un’istanza di ChatService (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il servizio ChatService venga
     * correttamente creato e inizializzato.
     */
    // AAA: Arrange
    // (La fase di arrangiamento è già stata eseguita nel beforeEach)

    // AAA: Act
    // (Non c'è un vero e proprio "Act" in quanto abbiamo già creato l'istanza nel beforeEach)

    // AAA: Assert
    expect(service).toBeTruthy();
  });

  it('Dovrebbe invertire correttamente la variabile booleana isUpdatedSubject quando viene chiamato checkFileUpdates (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che al richiamo di checkFileUpdates() 
     * il BehaviorSubject isUpdatedSubject venga invertito (true -> false, false -> true).
     */

    // AAA: Arrange
    let currentValue!: boolean;
    service.isUpdated$.subscribe(value => (currentValue = value));
    const initialValue = currentValue;

    // AAA: Act
    service.checkFileUpdates();

    // AAA: Assert
    expect(currentValue).toBe(!initialValue);
  });

  it('Dovrebbe restituire e impostare correttamente il valore di lastMessageTimestamp (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il metodo setLastMessageTimestamp()
     * imposti correttamente un valore e getLastMessageTimestamp() lo restituisca.
     */

    // AAA: Arrange
    const now = Date.now();

    // AAA: Act
    service.setLastMessageTimestamp(now);

    // AAA: Assert
    expect(service.getLastMessageTimestamp()).toBe(now);
  });

  // ==============================================================================
  //                              TEST DI INTEGRAZIONE
  // ==============================================================================

  it('Dovrebbe chiamare correttamente l’endpoint POST /api/chat e gestire la risposta (Integration Test) - AAA', () => {
    /**
     * In questo test di integrazione verifichiamo la chiamata HTTP reale 
     * al servizio /api/chat e la gestione della risposta da parte del servizio.
     */

    // AAA: Arrange
    const fakeReply = { response: 'Risposta dal server' };
    let actualReply: string | undefined;

    // AAA: Act
    service.sendMessage('Hello').subscribe(res => {
      actualReply = res.response;
    });
    const req = httpMock.expectOne('http://localhost:5000/api/chat');
    req.flush(fakeReply);

    // AAA: Assert
    expect(req.request.method).toBe('POST');
    expect(actualReply).toBe('Risposta dal server');
  });

  it('Dovrebbe chiamare correttamente l’endpoint POST /api/get_next_possible_questions e gestirne la risposta (Integration Test) - AAA', () => {
    /**
     * In questo test di integrazione verifichiamo che la chiamata
     * /api/get_next_possible_questions risponda correttamente 
     * e che il servizio gestisca i dati ricevuti.
     */

    // AAA: Arrange
    const mockSuggestions = ['Cont1', 'Cont2'];
    let result: string[] = [];
    service.getContinuationSuggestions({ question: 'Q', answer: 'A', quantity: 3 })
      .subscribe(res => (result = Object.values(res)));
    const req = httpMock.expectOne('http://localhost:5000/api/get_next_possible_questions');

    // AAA: Act
    req.flush(mockSuggestions);

    // AAA: Assert
    expect(req.request.method).toBe('POST');
    expect(result).toEqual(mockSuggestions);
  });

  it('Dovrebbe gestire correttamente il metodo loadLastLoadOutcome (Integration Test) - AAA', () => {
    /**
     * In questo test di integrazione verifichiamo la chiamata
     * /api/get_last_load_outcome e controlliamo che la risposta 
     * venga gestita correttamente dal servizio.
     */

    // AAA: Arrange
    const consoleSpy = spyOn(console, 'log');
    const mockOutcomeTrue = true;

    // AAA: Act
    service.loadLastLoadOutcome();
    const req = httpMock.expectOne('http://localhost:5000/api/get_last_load_outcome');
    req.flush(mockOutcomeTrue);

    // AAA: Assert
    expect(req.request.method).toBe('POST');
    expect(consoleSpy).toHaveBeenCalledWith(true);
  });
});
