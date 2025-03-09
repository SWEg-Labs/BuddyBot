import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatSuggestionsComponent } from './chat-suggestions.component';
import { ChatService } from '../chat.service';
import { of, throwError } from 'rxjs';

describe('ChatSuggestionsComponent', () => {
  let component: ChatSuggestionsComponent;
  let fixture: ComponentFixture<ChatSuggestionsComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    chatServiceSpy = jasmine.createSpyObj<ChatService>(
      'ChatService',
      ['getContinuationSuggestions']
    );
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of([]));

    await TestBed.configureTestingModule({
      imports: [ChatSuggestionsComponent],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatSuggestionsComponent);
    component = fixture.componentInstance;
  });

  // Test di Unità
  it('Verifica che venga creata correttamente un’istanza di ChatSuggestionsComponent', () => {
    // Arrange
    component.lastMessageTimestamp = Date.now() - 6 * 60 * 1000;

    // Act
    fixture.detectChanges();

    // Assert
    expect(component).toBeTruthy();
  });
  
  // DA SOSTITUIRE CON UN TEST DIVERSO PER LA CONTINUAZIONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  // Test di Integrazione
  it('Verifica che, se la variabile lastMessageTimestamp di ChatSuggestionsComponent contiene un timestamp recente di massimo 5 minuti' +
    'venga chiamato ChatService per caricare i suggerimenti di continuazione', () => {
    // Arrange
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of(['Cont1', 'Cont2']));
    component.lastMessageTimestamp = Date.now();

    // Act
    fixture.detectChanges();

    // Assert
    expect(component.showInitial).toBeFalse();
    expect(component.continuationSuggestions).toEqual(['Cont1', 'Cont2']);
  });

  // Test di Integrazione
  it('Verifica che, se ChatService segnala un errore di caricamento suggerimenti, ChatSuggestionsComponent stampi'+
    'un messaggio di errore', () => {
    // Arrange
    chatServiceSpy.getContinuationSuggestions.and.returnValue(throwError(() => new Error('Errore')));
    component.lastMessageTimestamp = Date.now();

    // Act
    fixture.detectChanges();

    // Assert
    expect(component.loadError).toBeTrue();
  });

  // Test di Unità
  it('Verifica che, quando l’utente clicca un suggerimento, in ChatSuggestionsComponent venga emesso l’evento ' +
    'suggestionClicked', () => {
    // Arrange
    spyOn(component.suggestionClicked, 'emit');

    // Act
    component.onSuggestionClick('Prova');

    // Assert
    expect(component.suggestionClicked.emit).toHaveBeenCalledWith('Prova');
  });
});
