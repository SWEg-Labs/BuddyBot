import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ChatService } from './chat.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('ChatService', () => {
  let service: ChatService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // Arrange:
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ChatService],
    });
    service = TestBed.inject(ChatService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    // Act:
    httpMock.verify();
  });


  // ------------------------------------------------------
  // Test di integrazione
  // ------------------------------------------------------

  describe('Test di integrazione', () => {
    it("Verifica che il metodo sendMessage di ChatService chiami l’endpoint POST /api/chat e ne gestisca la risposta", () => {
      // Arrange:
      const testMessage = "Hello";
      const responseData = { response: "World" };
      // Act:
      service.sendMessage(testMessage).subscribe(response => {
        // Assert:
        expect(response).toEqual(responseData);
      });
      const req = httpMock.expectOne("http://localhost:5000/api/chat");
      expect(req.request.method).toBe("POST");
      expect(req.request.body).toEqual({ message: testMessage });
      req.flush(responseData);
    });

    it("Verifica che il metodo getContinuationSuggestions di ChatService chiami l’endpoint POST " +
      "/api/get_next_possible_questions e ne gestisca la risposta", () => {
      // Arrange:
      const payload = { question: "Q", answer: "A", quantity: 3 };
      const responseData = { 0: "Suggerimento1", 1: "Suggerimento2", 2: "Suggerimento3" };
      // Act:
      service.getContinuationSuggestions(payload).subscribe(response => {
        // Assert:
        expect(response).toEqual(responseData);
      });
      const req = httpMock.expectOne("http://localhost:5000/api/get_next_possible_questions");
      expect(req.request.method).toBe("POST");
      expect(req.request.body).toEqual(payload);
      req.flush(responseData);
    });

    it("Verifica che il metodo getContinuationSuggestions di ChatService gestisca correttamente l'errore ricevuto " +
      "dall'endpoint POST /api/get_next_possible_questions", fakeAsync(() => {
      // Arrange:
      const payload = { question: "Q", answer: "A", quantity: 3 };
      let errorResponse: any;
      // Act:
      service.getContinuationSuggestions(payload).subscribe({
        next: () => {},
        error: (err) => errorResponse = err,
      });
      const req = httpMock.expectOne("http://localhost:5000/api/get_next_possible_questions");
      req.flush("Error", { status: 500, statusText: "Server Error" });
      tick();
      // Assert:
      expect(errorResponse).toBeTruthy();
    }));
  });


  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------

  describe('Test di unità', () => {
    it("Verifica che ChatService restituisca e imposti correttamente il valore dell'attributo lastMessageTimestamp", () => {
      // Arrange:
      const oldTimestamp = service.getLastMessageTimestamp();
      const newTimestamp = oldTimestamp + 1000;
      // Act:
      service.setLastMessageTimestamp(newTimestamp);
      // Assert:
      expect(service.getLastMessageTimestamp()).toBe(newTimestamp);
    });

    it("Verifica che il metodo sendMessage di ChatService aggiorni correttamente l'attributo lastMessageTimestamp", fakeAsync(() => {
      // Arrange:
      const oldTimestamp = service.getLastMessageTimestamp();
      tick(50);
      const testMessage = "Hello";
      // Act:
      service.sendMessage(testMessage).subscribe();
      const req = httpMock.expectOne("http://localhost:5000/api/chat");
      req.flush({ response: "World" });
      tick();
      // Assert:
      expect(service.getLastMessageTimestamp()).toBeGreaterThan(oldTimestamp);
    }));

    it("Verifica che il metodo sendMessage di ChatService invochi il metodo setLastMessageTimestamp", () => {
      // Arrange:
      spyOn(service, 'setLastMessageTimestamp').and.callThrough();
      const testMessage = "Hello";
      // Act:
      service.sendMessage(testMessage).subscribe();
      const req = httpMock.expectOne("http://localhost:5000/api/chat");
      req.flush({ response: "World" });
      // Assert:
      expect(service.setLastMessageTimestamp).toHaveBeenCalled();
    });
  });
});
