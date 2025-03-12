import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatSuggestionsComponent } from './chat-suggestions.component';
import { ChatService } from '../chat.service';
import { of, throwError } from 'rxjs';

describe('ChatSuggestionsComponent', () => {
  let component: ChatSuggestionsComponent;
  let fixture: ComponentFixture<ChatSuggestionsComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange
    chatServiceSpy = jasmine.createSpyObj<ChatService>('ChatService', ['getContinuationSuggestions']);
    chatServiceSpy.getContinuationSuggestions.and.returnValue(
      of({ su1: 'Suggerimento1', su2: 'Suggerimento2' })
    );
    await TestBed.configureTestingModule({
      imports: [ChatSuggestionsComponent],
      providers: [{ provide: ChatService, useValue: chatServiceSpy }]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatSuggestionsComponent);
    component = fixture.componentInstance;
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================

  it('Dovrebbe creare correttamente un’istanza di ChatSuggestionsComponent (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il componente ChatSuggestionsComponent
     * venga creato senza errori.
     */
    // AAA: Act
    fixture.detectChanges();

    // AAA: Assert
    expect(component).toBeTruthy();
  });

  it('Dovrebbe emettere l’evento suggestionClicked quando si clicca un suggerimento (Unit Test) - AAA', () => {
    /**
     * In questo test controlliamo che il componente emetta l’evento "suggestionClicked"
     * con il testo corretto quando si clicca su un suggerimento.
     */

    // AAA: Arrange
    spyOn(component.suggestionClicked, 'emit');

    // AAA: Act
    component.onSuggestionClick('Prova');

    // AAA: Assert
    expect(component.suggestionClicked.emit).toHaveBeenCalledWith('Prova');
  });

  it('Dovrebbe non caricare i suggerimenti se hideSuggestions=true (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che, se la proprietà hideSuggestions è impostata a true,
     * non vengano caricati i suggerimenti di continuazione.
     */

    // AAA: Arrange
    component.hideSuggestions = true;
    component.question = 'Q?';
    component.answer = 'A!';

    // AAA: Act
    fixture.detectChanges();

    // AAA: Assert
    expect(component.continuationSuggestions.length).toBe(0);
    expect(component.loadError).toBeFalse();
  });

  // ==============================================================================
  //                              TEST DI INTEGRAZIONE
  // ==============================================================================

  it('Dovrebbe caricare correttamente i suggerimenti di continuazione se question e answer sono valide e hideSuggestions=false (Integration Test) - AAA', () => {
    /**
     * In questo test di integrazione verifichiamo che, quando le proprietà question e answer
     * sono valorizzate e hideSuggestions è false, vengano effettivamente caricati i suggerimenti.
     */

    // AAA: Arrange
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of(['Cont1', 'Cont2'] as any));
    component.question = 'Domanda?';
    component.answer = 'Risposta!';
    component.hideSuggestions = false;

    // AAA: Act
    fixture.detectChanges();

    // AAA: Assert
    expect(component.continuationSuggestions).toEqual(['Cont1', 'Cont2']);
  });

  it('Dovrebbe gestire un errore di caricamento dei suggerimenti di continuazione (Integration Test) - AAA', () => {
    /**
     * In questo test di integrazione verifichiamo che il componente gestisca correttamente
     * un errore quando la chiamata getContinuationSuggestions() fallisce.
     */

    // AAA: Arrange
    chatServiceSpy.getContinuationSuggestions.and.returnValue(throwError(() => new Error('Errore')));
    component.question = 'Domanda?';
    component.answer = 'Risposta!';
    component.hideSuggestions = false;

    // AAA: Act
    fixture.detectChanges();

    // AAA: Assert
    expect(component.loadError).toBeTrue();
  });
});
