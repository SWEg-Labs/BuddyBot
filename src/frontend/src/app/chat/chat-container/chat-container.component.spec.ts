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
    it("Verifica che ngOnInit richiami loadOldMessages e loadLastLoadOutcome", () => {
      // Arrange:
      spyOn(component, 'loadOldMessages');
      // Act:
      component.ngOnInit();
      // Assert:
      expect(component.loadOldMessages).toHaveBeenCalledWith(50);
      expect(mockDatabaseService.loadLastLoadOutcome).toHaveBeenCalled();
    });

    it("Verifica che loadOldMessages ordini e formatti correttamente i messaggi", fakeAsync(() => {
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

    it("Verifica che onScrollChange aggiorni showScrollToBottom", () => {
      // Arrange:
      // Act:
      component.onScrollChange(true);
      // Assert:
      expect(component.showScrollToBottom).toBeTrue();
    });

    it("Verifica che onSendMessage gestisca correttamente il caso di invio con risposta positiva", fakeAsync(() => {
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

    it("Verifica che onSendMessage gestisca correttamente il caso di invio con errore", fakeAsync(() => {
      // Arrange:
      const inputText = "ErroreTest";
      const trimmedText = "ErroreTest";
      mockChatService.sendMessage.and.returnValue(throwError(() => new Error("Error")));
      mockDatabaseService.saveMessage.and.returnValue(of({ status: true }));
      spyOn(component, 'scrollToBottom');
      // Act:
      component.onSendMessage(inputText);
      tick(0);
      // Assert:
      expect(component.messages.some(m => m.sender === MessageSender.CHATBOT && m.content === "C’è stato un errore!")).toBeTrue();
      expect(component.isLoading).toBeFalse();
      expect(component.scrollToBottom).toHaveBeenCalled();
    }));

    it("Verifica che onSuggestionClicked invochi onSendMessage con il suggerimento", () => {
      // Arrange:
      spyOn(component, 'onSendMessage');
      const suggestion = "Suggerimento";
      // Act:
      component.onSuggestionClicked(suggestion);
      // Assert:
      expect(component.onSendMessage).toHaveBeenCalledWith(suggestion);
    });

    it("Verifica che formatResponse trasformi correttamente la stringa", () => {
      // Arrange:
      const input = "Test **grassetto** http://esempio.com";
      // Act:
      const output = component.formatResponse(input);
      // Assert:
      expect(output).toContain("<strong>grassetto</strong>");
      expect(output).toContain('<a href="http://esempio.com" target="_blank">http://esempio.com</a>');
    });

    it("Verifica che scrollToBottom invochi il metodo scrollToBottom di messagesComponent", () => {
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
    let localComponent: ChatContainerComponent;
    let localChatService: any;
    let localDatabaseService: any;
    let localSanitizer: any;

    beforeEach(() => {
      // Arrange:
      localChatService = {
        sendMessage: jasmine.createSpy('sendMessage')
      };
      localDatabaseService = {
        getMessages: jasmine.createSpy('getMessages'),
        saveMessage: jasmine.createSpy('saveMessage'),
        loadLastLoadOutcome: jasmine.createSpy('loadLastLoadOutcome')
      };
      localSanitizer = {
        bypassSecurityTrustHtml: (value: string) => value
      };
      // Arrange:
      localComponent = new ChatContainerComponent(localChatService, localSanitizer, localDatabaseService);
      localComponent.messagesComponent = { scrollToBottom: jasmine.createSpy('scrollToBottom') } as any;
    });

    it("Verifica che ngOnInit richiami loadOldMessages e loadLastLoadOutcome", () => {
      // Arrange:
      spyOn(localComponent, 'loadOldMessages');
      // Act:
      localComponent.ngOnInit();
      // Assert:
      expect(localComponent.loadOldMessages).toHaveBeenCalledWith(50);
      expect(localDatabaseService.loadLastLoadOutcome).toHaveBeenCalled();
    });

    it("Verifica che onScrollChange aggiorni showScrollToBottom (unità)", () => {
      // Arrange:
      // Act:
      localComponent.onScrollChange(false);
      // Assert:
      expect(localComponent.showScrollToBottom).toBeFalse();
    });

    it("Verifica che onSendMessage non faccia nulla se il testo è vuoto", () => {
      // Arrange:
      const initialMessagesLength = localComponent.messages.length;
      // Act:
      localComponent.onSendMessage("   ");
      // Assert:
      expect(localComponent.messages.length).toBe(initialMessagesLength);
    });

    it("Verifica che onSendMessage gestisca correttamente il caso positivo", fakeAsync(() => {
      // Arrange:
      const inputText = "UnitTest";
      const trimmedText = "UnitTest";
      const botResponse = { response: "RispostaUnitBot" };
      localChatService.sendMessage.and.returnValue(of(botResponse));
      localDatabaseService.saveMessage.and.returnValue(of({ status: true }));
      spyOn(localComponent, 'scrollToBottom');
      // Act:
      localComponent.onSendMessage(inputText);
      tick(0);
      // Assert:
      expect(localComponent.messages.some(m => m.sender === MessageSender.USER && m.content === trimmedText)).toBeTrue();
      expect(localChatService.sendMessage).toHaveBeenCalledWith(trimmedText);
      expect(localComponent.messages.some(m => m.sender === MessageSender.CHATBOT && m.content === botResponse.response)).toBeTrue();
      expect(localComponent.isLoading).toBeFalse();
      expect(localComponent.lastUserQuestion).toBe(trimmedText);
      expect(localComponent.lastBotAnswer).toBe(botResponse.response);
      expect(localComponent.hideSuggestions).toBeFalse();
      expect(localComponent.scrollToBottom).toHaveBeenCalled();
    }));

    it("Verifica che onSendMessage gestisca correttamente il caso di errore", fakeAsync(() => {
      // Arrange:
      const inputText = "UnitError";
      localChatService.sendMessage.and.returnValue(throwError(() => new Error("Error")));
      localDatabaseService.saveMessage.and.returnValue(of({ status: true }));
      spyOn(localComponent, 'scrollToBottom');
      // Act:
      localComponent.onSendMessage(inputText);
      tick(0);
      // Assert:
      expect(localComponent.messages.some(m => m.sender === MessageSender.CHATBOT && m.content === "C’è stato un errore!")).toBeTrue();
      expect(localComponent.isLoading).toBeFalse();
      expect(localComponent.scrollToBottom).toHaveBeenCalled();
    }));

    it("Verifica che onSuggestionClicked invochi onSendMessage", () => {
      // Arrange:
      spyOn(localComponent, 'onSendMessage');
      const suggestion = "UnitSuggerimento";
      // Act:
      localComponent.onSuggestionClicked(suggestion);
      // Assert:
      expect(localComponent.onSendMessage).toHaveBeenCalledWith(suggestion);
    });

    it("Verifica che formatResponse trasformi correttamente la stringa", () => {
      // Arrange:
      const input = "Unit **Bold** http://link.com";
      // Act:
      const output = localComponent.formatResponse(input);
      // Assert:
      expect(output).toContain("<strong>Bold</strong>");
      expect(output).toContain('<a href="http://link.com" target="_blank">http://link.com</a>');
    });

    it("Verifica che scrollToBottom invochi il metodo scrollToBottom di messagesComponent", () => {
      // Arrange:
      localComponent.messagesComponent = { scrollToBottom: jasmine.createSpy('scrollToBottom') } as any;
      // Act:
      localComponent.scrollToBottom();
      // Assert:
      expect(localComponent.messagesComponent.scrollToBottom).toHaveBeenCalled();
    });
  });
});
