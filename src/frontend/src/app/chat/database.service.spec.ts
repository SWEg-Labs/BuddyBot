import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { DatabaseService } from './database.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { Message, MessageSender } from '../models/message.model';
import { LastLoadOutcome } from '../models/badge.model';

describe('DatabaseService', () => {
  let service: DatabaseService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // Arrange:
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DatabaseService],
    });
    service = TestBed.inject(DatabaseService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    // Act:
    httpMock.verify();
  });

  describe('getMessages', () => {
    it("Verifica che getMessages mappi correttamente la risposta in un array di Message", () => {
      // Arrange:
      const responseArray = [
        { content: "Ciao", timestamp: "2023-01-01T00:00:00Z", sender: "USER" },
        { content: "Salve", timestamp: "2023-01-01T00:01:00Z", sender: "CHATBOT" }
      ];
      // Act:
      service.getMessages(2).subscribe(messages => {
        // Assert:
        expect(messages.length).toBe(2);
        expect(messages[0].content).toBe("Ciao");
        expect(messages[0].sender).toBe(MessageSender.USER);
        expect(new Date(messages[0].timestamp).toISOString()).toBe("2023-01-01T00:00:00.000Z");
        expect(messages[1].content).toBe("Salve");
        expect(messages[1].sender).toBe(MessageSender.CHATBOT);
      });
      const req = httpMock.expectOne("http://localhost:5000/api/get_messages");
      expect(req.request.method).toBe("POST");
      expect(req.request.body).toEqual({ quantity: 2 });
      req.flush(responseArray);
    });
  });

  describe('saveMessage', () => {
    it("Verifica che saveMessage invii il payload corretto e gestisca la risposta", () => {
      // Arrange:
      const message = new Message("Test", new Date("2023-01-01T00:00:00Z"), MessageSender.USER);
      const responseData = { status: true };
      // Act:
      service.saveMessage(message).subscribe(response => {
        // Assert:
        expect(response).toEqual(responseData);
      });
      const req = httpMock.expectOne("http://localhost:5000/api/save_message");
      expect(req.request.method).toBe("POST");
      expect(req.request.body).toEqual({
        content: message.content,
        sender: message.sender,
        timestamp: message.timestamp
      });
      req.flush(responseData);
    });
  });

  describe('loadLastLoadOutcome', () => {
    it("Verifica che loadLastLoadOutcome imposti TRUE se la risposta è 'True'", fakeAsync(() => {
      // Arrange:
      let outcome: LastLoadOutcome | undefined;
      service.lastLoadOutcome$.subscribe(val => outcome = val);
      // Act:
      service.loadLastLoadOutcome();
      const req = httpMock.expectOne("http://localhost:5000/api/get_last_load_outcome");
      expect(req.request.method).toBe("POST");
      req.flush("True");
      tick();
      // Assert:
      expect(outcome).toBe(LastLoadOutcome.TRUE);
    }));

    it("Verifica che loadLastLoadOutcome imposti FALSE se la risposta è 'False'", fakeAsync(() => {
      // Arrange:
      let outcome: LastLoadOutcome | undefined;
      service.lastLoadOutcome$.subscribe(val => outcome = val);
      // Act:
      service.loadLastLoadOutcome();
      const req = httpMock.expectOne("http://localhost:5000/api/get_last_load_outcome");
      req.flush("False");
      tick();
      // Assert:
      expect(outcome).toBe(LastLoadOutcome.FALSE);
    }));

    it("Verifica che loadLastLoadOutcome imposti ERROR se la risposta non è 'True' o 'False'", fakeAsync(() => {
      // Arrange:
      let outcome: LastLoadOutcome | undefined;
      service.lastLoadOutcome$.subscribe(val => outcome = val);
      // Act:
      service.loadLastLoadOutcome();
      const req = httpMock.expectOne("http://localhost:5000/api/get_last_load_outcome");
      req.flush("Unexpected");
      tick();
      // Assert:
      expect(outcome).toBe(LastLoadOutcome.ERROR);
    }));

    it("Verifica che loadLastLoadOutcome imposti ERROR in caso di errore", fakeAsync(() => {
      // Arrange:
      let outcome: LastLoadOutcome | undefined;
      service.lastLoadOutcome$.subscribe(val => outcome = val);
      // Act:
      service.loadLastLoadOutcome();
      const req = httpMock.expectOne("http://localhost:5000/api/get_last_load_outcome");
      req.flush("Error", { status: 500, statusText: "Server Error" });
      tick();
      // Assert:
      expect(outcome).toBe(LastLoadOutcome.ERROR);
    }));
  });
});
