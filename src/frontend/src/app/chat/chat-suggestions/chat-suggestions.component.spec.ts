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
    it("Verifica che il componente venga creato", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che, se question e answer sono validi e hideSuggestions è false, vengano caricate le suggestions", fakeAsync(() => {
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
    }));

    it("Verifica che, se getContinuationSuggestions fallisce, loadError sia true", fakeAsync(() => {
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
    }));

    it("Verifica che, se hideSuggestions è true, le suggestions siano svuotate e loadError sia false", () => {
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
    });

    it("Verifica che ngOnChanges non reagisca se non ci sono cambiamenti rilevanti", () => {
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

    it("Verifica che onSuggestionClick emetta il valore corretto", () => {
      // Arrange:
      spyOn(component.suggestionClicked, 'emit');
      const testText = "Test Suggerimento";
      // Act:
      component.onSuggestionClick(testText);
      // Assert:
      expect(component.suggestionClicked.emit).toHaveBeenCalledWith(testText);
    });
  });

  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------
  describe('Test di unità', () => {
    it("Verifica che l'istanza del componente sia definita", () => {
      // Arrange:
      const localComponent = new ChatSuggestionsComponent(fakeChatService);
      // Act:
      // Assert:
      expect(localComponent).toBeDefined();
    });

    it("Verifica che canLoadSuggestions restituisca true per input validi", () => {
      // Arrange:
      component.question = "Test";
      component.answer = "Risposta";
      // Act:
      const canLoad = (component as any).canLoadSuggestions();
      // Assert:
      expect(canLoad).toBeTrue();
    });

    it("Verifica che canLoadSuggestions restituisca false se question è vuota", () => {
      // Arrange:
      component.question = "   ";
      component.answer = "Risposta";
      // Act:
      const canLoad = (component as any).canLoadSuggestions();
      // Assert:
      expect(canLoad).toBeFalse();
    });

    it("Verifica che canLoadSuggestions restituisca false se answer è vuota", () => {
      // Arrange:
      component.question = "Domanda";
      component.answer = "";
      // Act:
      const canLoad = (component as any).canLoadSuggestions();
      // Assert:
      expect(canLoad).toBeFalse();
    });

    it("Verifica che getContinuationSuggestions non venga chiamato se canLoadSuggestions restituisce false", () => {
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
  });
});
