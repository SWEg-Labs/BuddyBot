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
  it('deve creare correttamente l’istanza di ChatSuggestionsComponent', () => {
    component.lastMessageTimestamp = Date.now() - 6 * 60 * 1000;
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('deve mostrare i suggerimenti iniziali se lastMessageTimestamp è più vecchio di 5 minuti', () => {
    component.lastMessageTimestamp = Date.now() - 6 * 60 * 1000;
    fixture.detectChanges();
    expect(component.showInitial).toBeTrue();
  });

  // Test di Integrazione
  it('deve caricare i suggerimenti di continuazione se lastMessageTimestamp è recente', () => {
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of(['Cont1', 'Cont2']));
    component.lastMessageTimestamp = Date.now();
    fixture.detectChanges();
    expect(component.showInitial).toBeFalse();
    expect(component.continuationSuggestions).toEqual(['Cont1', 'Cont2']);
  });

  // Test di Integrazione
  it('deve gestire un errore di caricamento suggerimenti', () => {
    chatServiceSpy.getContinuationSuggestions.and.returnValue(throwError(() => new Error('Errore')));
    component.lastMessageTimestamp = Date.now();
    fixture.detectChanges();
    expect(component.loadError).toBeTrue();
  });

  // Test di Unità
  it('deve emettere suggestionClicked quando viene cliccato un suggerimento', () => {
    spyOn(component.suggestionClicked, 'emit');
    component.onSuggestionClick('Prova');
    expect(component.suggestionClicked.emit).toHaveBeenCalledWith('Prova');
  });
});
