import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ChatContainerComponent } from './chat-container.component';
import { ChatService } from '../chat.service';
import { DatabaseService } from '../database.service';
import { DomSanitizer } from '@angular/platform-browser';
import { of, throwError } from 'rxjs';
import { Message, MessageSender } from '../../models/message.model';

describe('ChatContainerComponent', () => {
  let component: ChatContainerComponent;
  let fixture: ComponentFixture<ChatContainerComponent>;
  let mockChatService: any;
  let mockDatabaseService: any;
  let mockSanitizer: any;

  beforeEach(async () => {
    // Arrange:
    mockChatService = {
      sendMessage: jasmine.createSpy('sendMessage')
    };
    mockDatabaseService = {
      getMessages: jasmine.createSpy('getMessages'),
      saveMessage: jasmine.createSpy('saveMessage'),
      loadLastLoadOutcome: jasmine.createSpy('loadLastLoadOutcome')
    };
    mockSanitizer = {
      bypassSecurityTrustHtml: (value: string) => value
    };
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [ChatContainerComponent],
      providers: [
        { provide: ChatService, useValue: mockChatService },
        { provide: DatabaseService, useValue: mockDatabaseService },
        { provide: DomSanitizer, useValue: mockSanitizer },
      ]
    }).compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(ChatContainerComponent);
    component = fixture.componentInstance;
    // Arrange:
    component.messagesComponent = { scrollToBottom: jasmine.createSpy('scrollToBottom') } as any;
  });


  // ------------------------------------------------------
  // Test di integrazione
  // ------------------------------------------------------

  describe('Test di integrazione', () => {
    it("Verifica che l'evento ngOnInit di ChatContainerComponent richiami il metodo loadLastLoadOutcome di DatabaseService", () => {
      // Arrange:
      spyOn(component, 'loadOldMessages');
      // Act:
      component.ngOnInit();
      // Assert:
      expect(mockDatabaseService.loadLastLoadOutcome).toHaveBeenCalled();
    });

    it("Verifica che il metodo loadOldMessages di ChatContainerComponent ordini e formatti correttamente i messaggi " +
      "ricevuti da DatabaseService", fakeAsync(() => {
      // Arrange:
      const msg1 = new Message('B', new Date(2020, 1, 2), MessageSender.USER);
      const msg2 = new Message('A', new Date(2020, 1, 1), MessageSender.CHATBOT);
      mockDatabaseService.getMessages.and.returnValue(of([msg1, msg2]));
      spyOn(component, 'scrollToBottom');
      // Act:
      component.loadOldMessages(2);
      tick(0);
      // Assert:
      expect(component.messages.length).toBe(2);
      expect(component.messages[0].content).toBe('A');
      expect(component.messages[1].content).toBe('B');
      expect(component.messages[0].sanitizedContent).toContain('A');
      expect(component.scrollToBottom).toHaveBeenCalled();
    }));

    it("Verifica che il metodo loadOldMessages di ChatContainerComponent imposti errorMessage in caso di errore " +
      "nel recupero dei messaggi restituito da DatabaseService", fakeAsync(() => {
      // Arrange:
      mockDatabaseService.getMessages.and.returnValue(throwError(() => new Error("Test Error")));
      // Act:
      component.loadOldMessages(50);
      tick(0);
      // Assert:
      expect(component.errorMessage).toBe("Errore nel recupero dello storico dei messaggi");
    }));

    it("Verifica che il metodo loadOldMessages di ChatContainerComponent resetti errorMessage se il recupero " +
      "dei messaggi da DatabaseService ha successo", fakeAsync(() => {
      // Arrange:
      const msg1 = new Message('Test message', new Date(), MessageSender.USER);
      // Imposto un errore preesistente:
      component.errorMessage = "Errore nel recupero dello storico dei messaggi";
      mockDatabaseService.getMessages.and.returnValue(of([msg1]));
      // Act:
      component.loadOldMessages(50);
      tick(0);
      // Assert:
      expect(component.errorMessage).toBe('');
    }));

    it("Verifica che il metodo onSendMessage di ChatContainerComponent gestisca correttamente il caso di invio di una domanda " +
      "a ChatService a seguito della quale viene restituita una risposta positiva", fakeAsync(() => {
      // Arrange:
      const inputText = "Test";
      const trimmedText = "Test";
      const botResponse = { response: "Risposta Bot" };
      mockChatService.sendMessage.and.returnValue(of(botResponse));
      mockDatabaseService.saveMessage.and.returnValue(of({ status: true }));
      spyOn(component, 'scrollToBottom');
      // Act:
      component.onSendMessage(" " + inputText + " ");
      tick(0);
      // Assert:
      expect(component.messages.some(m => m.sender === MessageSender.USER && m.content === trimmedText)).toBeTrue();
      expect(mockChatService.sendMessage).toHaveBeenCalledWith(trimmedText);
      expect(component.messages.some(m => m.sender === MessageSender.CHATBOT && m.content === botResponse.response)).toBeTrue();
      expect(component.isLoading).toBeFalse();
      expect(component.lastUserQuestion).toBe(trimmedText);
      expect(component.lastBotAnswer).toBe(botResponse.response);
      expect(component.hideSuggestions).toBeFalse();
      expect(component.scrollToBottom).toHaveBeenCalled();
    }));

    it("Verifica che il metodo onSendMessage di ChatContainerComponent gestisca correttamente il caso di invio di una domanda " +
      "a ChatService a seguito della quale viene restituito un errore", fakeAsync(() => {
      // Arrange:
      const inputText = "ErroreTest";
      mockChatService.sendMessage.and.returnValue(throwError(() => new Error("Error")));
      mockDatabaseService.saveMessage.and.returnValue(of({ status: true }));
      spyOn(component, 'scrollToBottom');
      // Act:
      component.onSendMessage(inputText);
      tick(0);
      // Assert:
      expect(component.messages.some(m => m.sender === MessageSender.CHATBOT && m.content === "C'è stato un errore!")).toBeTrue();
      expect(component.isLoading).toBeFalse();
      expect(component.scrollToBottom).toHaveBeenCalled();
    }));

    it("Verifica che il metodo scrollToBottom di ChatContainerComponent invochi il metodo scrollToBottom di " +
      "ChatMessagesComponent", () => {
      // Arrange:
      component.messagesComponent = { scrollToBottom: jasmine.createSpy('scrollToBottom') } as any;
      // Act:
      component.scrollToBottom();
      // Assert:
      expect(component.messagesComponent.scrollToBottom).toHaveBeenCalled();
    });
  });


  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------

  describe('Test di unità', () => {

    it("Verifica che l'evento ngOnInit di ChatContainerComponent richiami il metodo loadOldMessages con l'intero 50 " +
      "come parametro", () => {
      // Arrange:
      spyOn(component, 'loadOldMessages');
      // Act:
      component.ngOnInit();
      // Assert:
      expect(component.loadOldMessages).toHaveBeenCalledWith(component.messagesPerPage, 1);
    });

    it("Verifica che il metodo onScrollChange di ChatContainerComponent, chiamato con valore true, " +
      "aggiorni l'attributo showScrollToBottom a true", () => {
      // Act:
      component.onScrollChange(true);
      // Assert:
      expect(component.showScrollToBottom).toBeTrue();
    });

    it("Verifica che il metodo onScrollChange di ChatContainerComponent, chiamato con valore false, " +
      "aggiorni l'attributo showScrollToBottom a false", () => {
      // Act:
      component.onScrollChange(false);
      // Assert:
      expect(component.showScrollToBottom).toBeFalse();
    });

    it("Verifica che il metodo onSendMessage di ChatContainerComponent non faccia nulla se il testo ricevuto in input è vuoto " +
      "oppure contiene solo spazi", () => {
      // Arrange:
      const initialMessagesLength = component.messages.length;
      // Act:
      component.onSendMessage("   ");
      // Assert:
      expect(component.messages.length).toBe(initialMessagesLength);
    });

    it("Verifica che il metodo onSuggestionClicked di ChatContainerComponent, invocato con un suggerimento, richiami il metodo" +
      " onSendMessage passando come parametro il suggerimento ricevuto", () => {
      // Arrange:
      spyOn(component, 'onSendMessage');
      const suggestion = "Suggerimento";
      // Act:
      component.onSuggestionClicked(suggestion);
      // Assert:
      expect(component.onSendMessage).toHaveBeenCalledWith(suggestion);
    });

    it("Verifica che il metodo formatResponse di ChatContainerComponent trasformi correttamente la stringa ricevuta in input", () => {
      // Arrange:
      const input = "Test **grassetto** http://esempio.com";
      // Act:
      const output = component.formatResponse(input);
      // Assert:
      expect(output).toContain("<strong>grassetto</strong>");
      expect(output).toContain('<a href="http://esempio.com" target="_blank">http://esempio.com</a>');
    });

    it("Verifica che il metodo loadOldMessages di ChatContainerComponent, in caso di errore nel recupero dei messaggi, imposti " +
      "l'attributo errorMessage come equivalente al messaggio di errore", fakeAsync(() => {
      // Arrange:
      mockDatabaseService.getMessages.and.returnValue(throwError(() => new Error("Test Error")));
      // Act:
      component.loadOldMessages(50);
      tick(0);
      // Assert:
      expect(component.errorMessage).toBe("Errore nel recupero dello storico dei messaggi");
    }));

    it("Verifica che il metodo loadOldMessages di ChatContainerComponent, se il recupero dei messaggi ha successo, resetti " +
      "l'attributo errorMessage ad una stringa vuota", fakeAsync(() => {
      // Arrange:
      const msg1 = new Message('UnitTest message', new Date(), MessageSender.USER);
      component.errorMessage = "Errore nel recupero dello storico dei messaggi";
      mockDatabaseService.getMessages.and.returnValue(of([msg1]));
      // Act:
      component.loadOldMessages(50);
      tick(0);
      // Assert:
      expect(component.errorMessage).toBe('');
    }));
  });
});
