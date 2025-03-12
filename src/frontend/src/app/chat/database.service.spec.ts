import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { DatabaseService } from './database.service';
import { Message, MessageSender } from '../models/message.model';
import { LastLoadOutcome } from '../models/badge.model';

describe('DatabaseService', () => {
  let service: DatabaseService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // AAA: Arrange
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DatabaseService],
    });
    service = TestBed.inject(DatabaseService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================
  it('Dovrebbe creare correttamente un’istanza di DatabaseService (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il servizio DatabaseService venga
     * creato correttamente e che l'istanza sia definita.
     */
    // AAA: Arrange
    // (Istanza già creata nel beforeEach)

    // AAA: Act
    // (Nessuna azione specifica)

    // AAA: Assert
    expect(service).toBeTruthy();
  });

  it('Dovrebbe inizializzare lastLoadOutcome$ con valore LastLoadOutcome.TRUE (Unit Test) - AAA', (done) => {
    /**
     * In questo test verifichiamo che la BehaviorSubject lastLoadOutcomeSubject
     * parta dal valore "LastLoadOutcome.TRUE".
     */
    // AAA: Arrange

    // AAA: Act
    service.lastLoadOutcome$.subscribe((outcome) => {
      // AAA: Assert
      expect(outcome).toBe(LastLoadOutcome.TRUE);
      done();
    });
  });

  // ==============================================================================
  //                              TEST DI INTEGRAZIONE
  // ==============================================================================
  it('Dovrebbe chiamare POST /api/get_messages e convertire la risposta in un array di Message (Integration Test) - AAA', () => {
    /**
     * In questo test verifichiamo che getMessages():
     * - invii una POST a /api/get_messages
     * - converta correttamente i dati in oggetti Message
     */
    // AAA: Arrange
    const mockResponse = [
      { content: 'Hello', sender: 'USER', timestamp: '2023-10-10T10:00:00Z' },
      { content: 'Hi', sender: 'CHATBOT', timestamp: '2023-10-10T10:00:05Z' },
    ];
    let actualMessages: Message[] | undefined;

    // AAA: Act
    service.getMessages(2).subscribe((messages) => {
      actualMessages = messages;
    });

    // Intercettiamo la richiesta HTTP
    const req = httpMock.expectOne('http://localhost:5000/api/get_messages');
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);

    // AAA: Assert
    expect(actualMessages).toBeDefined();
    expect(actualMessages?.length).toBe(2);
    expect(actualMessages?.[0].content).toBe('Hello');
    expect(actualMessages?.[0].sender).toBe(MessageSender.USER);
    expect(actualMessages?.[1].sender).toBe(MessageSender.CHATBOT);
  });

  it('Dovrebbe chiamare POST /api/save_message per salvare un messaggio (Integration Test) - AAA', () => {
    /**
     * In questo test verifichiamo che saveMessage():
     * - invii correttamente il payload
     * - gestisca la subscription e la risposta
     */
    // AAA: Arrange
    const testMessage = new Message('Salve', new Date('2023-10-10T10:00:00Z'), MessageSender.USER);
    const mockResponse = { status: true };
    let actualResponse: { status: boolean | string } | undefined;

    // AAA: Act
    service.saveMessage(testMessage).subscribe((res) => {
      actualResponse = res;
    });

    const req = httpMock.expectOne('http://localhost:5000/api/save_message');
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);

    // AAA: Assert
    expect(actualResponse?.status).toBeTrue();
    expect(req.request.body).toEqual({
      content: 'Salve',
      sender: 'USER',
      timestamp: new Date('2023-10-10T10:00:00Z'),
    });
  });

  it('Dovrebbe chiamare POST /api/get_last_load_outcome e gestire correttamente "True" (Integration Test) - AAA', () => {
    /**
     * In questo test verifichiamo che loadLastLoadOutcome():
     * - chiami /api/get_last_load_outcome
     * - setti lastLoadOutcomeSubject a LastLoadOutcome.TRUE se la risposta è "True"
     */
    // AAA: Arrange
    let outcome!: LastLoadOutcome;
    service.lastLoadOutcome$.subscribe((res) => (outcome = res));

    // AAA: Act
    service.loadLastLoadOutcome();
    const req = httpMock.expectOne('http://localhost:5000/api/get_last_load_outcome');
    expect(req.request.method).toBe('POST');
    req.flush('True');

    // AAA: Assert
    expect(outcome).toBe(LastLoadOutcome.TRUE);
  });

  it('Dovrebbe gestire correttamente la risposta "False" in loadLastLoadOutcome (Integration Test) - AAA', () => {
    /**
     * Verifichiamo che se la risposta è "False",
     * lastLoadOutcome$ venga impostato a LastLoadOutcome.FALSE.
     */
    // AAA: Arrange
    let outcome!: LastLoadOutcome;
    service.lastLoadOutcome$.subscribe((res) => (outcome = res));

    // AAA: Act
    service.loadLastLoadOutcome();
    const req = httpMock.expectOne('http://localhost:5000/api/get_last_load_outcome');
    req.flush('False');

    // AAA: Assert
    expect(outcome).toBe(LastLoadOutcome.FALSE);
  });

  it('Dovrebbe settare lastLoadOutcome=ERROR se la risposta non è né "True" né "False" (Integration Test) - AAA', () => {
    /**
     * Se la risposta dal server non è "True" o "False",
     * ci aspettiamo che lastLoadOutcome$ venga impostato a "ERROR".
     */
    // AAA: Arrange
    let outcome!: LastLoadOutcome;
    service.lastLoadOutcome$.subscribe((res) => (outcome = res));

    // AAA: Act
    service.loadLastLoadOutcome();
    const req = httpMock.expectOne('http://localhost:5000/api/get_last_load_outcome');
    req.flush('BOH');

    // AAA: Assert
    expect(outcome).toBe(LastLoadOutcome.ERROR);
  });

  it('Dovrebbe gestire correttamente l’errore di rete in loadLastLoadOutcome (Integration Test) - AAA', () => {
    /**
     * Se il server restituisce errore, lastLoadOutcome$ viene impostato a "ERROR".
     */
    // AAA: Arrange
    let outcome!: LastLoadOutcome;
    service.lastLoadOutcome$.subscribe((res) => (outcome = res));

    // AAA: Act
    service.loadLastLoadOutcome();
    const req = httpMock.expectOne('http://localhost:5000/api/get_last_load_outcome');
    req.error(new ErrorEvent('Network Error'), { status: 500 });

    // AAA: Assert
    expect(outcome).toBe(LastLoadOutcome.ERROR);
  });
});
