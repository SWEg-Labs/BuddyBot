import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ChatSuggestionsComponent } from './chat-suggestions.component';
import { ChatService } from '../chat.service';
import { of, throwError } from 'rxjs';
import { SimpleChange, SimpleChanges } from '@angular/core';

describe('ChatSuggestionsComponent', () => {
  let component: ChatSuggestionsComponent;
  let fixture: ComponentFixture<ChatSuggestionsComponent>;
  let fakeChatService: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange:
    fakeChatService = jasmine.createSpyObj('ChatService', ['getContinuationSuggestions']);
    await TestBed.configureTestingModule({
      imports: [ChatSuggestionsComponent],
      providers: [{ provide: ChatService, useValue: fakeChatService }],
    }).compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(ChatSuggestionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });


  // ------------------------------------------------------
  // Test di integrazione
  // ------------------------------------------------------

  describe('Test di integrazione', () => {
    it("Verifica che il metodo getContinuationSuggestions di ChatService non venga chiamato se il metodo canLoadSuggestions di " +
      "ChatSuggestionsComponent restituisce false", () => {
      // Arrange:
      component.question = "   ";
      component.answer = "Risposta";
      fakeChatService.getContinuationSuggestions.calls.reset();
      const changes: SimpleChanges = {
        question: new SimpleChange(undefined, component.question, true),
        answer: new SimpleChange(undefined, component.answer, true)
      };
      // Act:
      component.ngOnChanges(changes);
      // Assert:
      expect(fakeChatService.getContinuationSuggestions).not.toHaveBeenCalled();
    });

    it("Verifica che, se gli attributi question e answer di ChatSuggestionsComponent sono validi e l'attributo hideSuggestions è " +
      "false, vengano caricate le suggestions chiamando il metodo getContinuationSuggestions di ChatService", fakeAsync(() => {
      // Arrange:
      component.question = "Domanda di test";
      component.answer = "Risposta di test";
      component.hideSuggestions = false;
      const suggestionsResponse = { 0: "Suggerimento 1", 1: "Suggerimento 2", 2: "Suggerimento 3" };
      fakeChatService.getContinuationSuggestions.and.returnValue(of(suggestionsResponse));
      const changes: SimpleChanges = {
        question: new SimpleChange(undefined, component.question, true),
        answer: new SimpleChange(undefined, component.answer, true)
      };
      // Act:
      component.ngOnChanges(changes);
      tick();
      fixture.detectChanges();
      // Assert:
      expect(component.continuationSuggestions).toEqual(Object.values(suggestionsResponse));
      expect(component.loadError).toBeFalse();
      expect(component.errorMessage).toBe('');
    }));

    it("Verifica che, se il metodo getContinuationSuggestions di ChatService fallisce, l'attributo loadError di ChatSuggestionsComponent " +
      "venga impostato a true e venga impostato l'attributo errorMessage come equivalente al messaggio d'errore", fakeAsync(() => {
      // Arrange:
      component.question = "Domanda";
      component.answer = "Risposta";
      component.hideSuggestions = false;
      fakeChatService.getContinuationSuggestions.and.returnValue(throwError(() => new Error("Error")));
      const changes: SimpleChanges = {
        question: new SimpleChange(undefined, component.question, true),
        answer: new SimpleChange(undefined, component.answer, true)
      };
      // Act:
      component.ngOnChanges(changes);
      tick();
      fixture.detectChanges();
      // Assert:
      expect(component.loadError).toBeTrue();
      expect(component.errorMessage).toBe("Errore nella generazione delle domande per proseguire la conversazione");
    }));
  });


  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------

  describe('Test di unità', () => {
    it("Verifica che il componente ChatSuggestionsComponent venga creato", () => {
      // Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che l'istanza del componente ChatSuggestionsComponent sia definita", () => {
      // Arrange:
      const localComponent = new ChatSuggestionsComponent(fakeChatService);
      // Assert:
      expect(localComponent).toBeDefined();
    });

    it("Verifica che il metodo canLoadSuggestions di ChatSuggestionsComponent restituisca true per input validi", () => {
      // Arrange:
      component.question = "Test";
      component.answer = "Risposta";
      // Act:
      const canLoad = (component as any).canLoadSuggestions();
      // Assert:
      expect(canLoad).toBeTrue();
    });

    it("Verifica che il metodo canLoadSuggestions di ChatSuggestionsComponent restituisca false se l'attributo question è vuoto", () => {
      // Arrange:
      component.question = "   ";
      component.answer = "Risposta";
      // Act:
      const canLoad = (component as any).canLoadSuggestions();
      // Assert:
      expect(canLoad).toBeFalse();
    });

    it("Verifica che il metodo canLoadSuggestions di ChatSuggestionsComponent restituisca false se l'attributo answer è vuoto", () => {
      // Arrange:
      component.question = "Domanda";
      component.answer = "";
      // Act:
      const canLoad = (component as any).canLoadSuggestions();
      // Assert:
      expect(canLoad).toBeFalse();
    });

    it("Verifica che, se l'attributo hideSuggestions di ChatSuggestionsComponent è true, l'attributo continuationSuggestions " +
      "sia una lista e l'attributo loadError sia false", () => {
      // Arrange:
      component.hideSuggestions = true;
      component.continuationSuggestions = ["Suggerimento"];
      component.loadError = true;
      const changes: SimpleChanges = {
        hideSuggestions: new SimpleChange(undefined, true, true)
      };
      // Act:
      component.ngOnChanges(changes);
      // Assert:
      expect(component.continuationSuggestions).toEqual([]);
      expect(component.loadError).toBeFalse();
      expect(component.errorMessage).toBe('');
    });

    it("Verifica che il metodo ngOnChanges di ChatSuggestionsComponent non reagisca se non ci sono cambiamenti rilevanti", () => {
      // Arrange:
      component.question = "Domanda";
      component.answer = "Risposta";
      const changes: SimpleChanges = {
        unrelated: new SimpleChange(undefined, "valore", true)
      };
      // Act:
      component.ngOnChanges(changes);
      // Assert:
      expect(component.continuationSuggestions).toEqual([]);
    });

    it("Verifica che il metodo onSuggestionClick di ChatSuggestionsComponent emetta il testo corretto, corrispondente " +
      "alla domanda suggerita cliccata dall'utente", () => {
      // Arrange:
      spyOn(component.suggestionClicked, 'emit');
      const testText = "Test Suggerimento";
      // Act:
      component.onSuggestionClick(testText);
      // Assert:
      expect(component.suggestionClicked.emit).toHaveBeenCalledWith(testText);
    });
  });
});
