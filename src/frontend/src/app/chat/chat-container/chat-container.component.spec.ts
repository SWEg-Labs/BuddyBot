import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ChatContainerComponent } from './chat-container.component';
import { ChatService } from '../chat.service';
import { of, Observable } from 'rxjs';
import { delay } from 'rxjs/operators';

describe('ChatContainerComponent', () => {
  let component: ChatContainerComponent;
  let fixture: ComponentFixture<ChatContainerComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    chatServiceSpy = jasmine.createSpyObj<ChatService>(
      'ChatService',
      [
        'sendMessage',
        'getLastMessageTimestamp',
        'getContinuationSuggestions',
        'getInitialSuggestions',
        'checkFileUpdates',
        'setLastMessageTimestamp'
      ]
    );
    chatServiceSpy.isUpdated$ = of(true);
    chatServiceSpy.getLastMessageTimestamp.and.returnValue(Date.now());
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of([]));
    chatServiceSpy.getInitialSuggestions.and.returnValue(of([]));

    await TestBed.configureTestingModule({
      imports: [ChatContainerComponent],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // Test di Unità
  it('deve creare correttamente l’istanza di ChatContainerComponent', () => {
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('deve impostare showScrollToBottom correttamente in base all’evento di scroll', () => {
    component.onScrollChange(true);
    expect(component.showScrollToBottom).toBeTrue();
    component.onScrollChange(false);
    expect(component.showScrollToBottom).toBeFalse();
  });

  // Test di Integrazione
  it('deve inviare un messaggio, impostare isLoading e aggiungere risposta del bot', fakeAsync(() => {
    chatServiceSpy.sendMessage.and.returnValue(
      of({ response: 'RispostaBot' }).pipe(delay(50))
    );
    component.onSendMessage('Ciao');
    expect(component.messages[0].text).toBe('Ciao');
    expect(component.isLoading).toBeTrue();
    tick(50);
    expect(component.messages[1].text.toString()).toContain('RispostaBot');
    expect(component.isLoading).toBeFalse();
  }));

  // Test di Unità
  it('deve ignorare l’invio di messaggi vuoti', () => {
    component.onSendMessage('   ');
    expect(component.messages.length).toBe(0);
  });

  // Test di Integrazione
  it('deve gestire l’errore in caso di invio messaggio fallito', fakeAsync(() => {
    chatServiceSpy.sendMessage.and.returnValue(
      new Observable(subscriber => {
        subscriber.error('Errore di rete');
      })
    );
    component.onSendMessage('Test');
    tick();
    expect(component.messages[1].text).toBe('C’è stato un errore!');
    expect(component.isLoading).toBeFalse();
  }));

  // Test di Unità
  it('deve inoltrare correttamente un suggerimento al metodo onSendMessage', () => {
    spyOn(component, 'onSendMessage');
    component.onSuggestionClicked('Suggerimento');
    expect(component.onSendMessage).toHaveBeenCalledWith('Suggerimento');
  });
});
