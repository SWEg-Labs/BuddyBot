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
        'checkFileUpdates',
        'setLastMessageTimestamp'
      ]
    );
    chatServiceSpy.isUpdated$ = of(true);
    chatServiceSpy.getLastMessageTimestamp.and.returnValue(Date.now());
    chatServiceSpy.getContinuationSuggestions.and.returnValue(
      of({ "Cont1": "Come stai?", "Cont2": "Hai altre domande?" })
    );
    

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
  it('Verifica che venga creata correttamente un’istanza di ChatContainerComponent', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('Verifica che, alla chiamata dell’evento onScrollChange di ChatContainerComponent, la variabile showScrollToBottom venga ' +
    'impostata correttamente', () => {
    // Act
    component.onScrollChange(true);

    // Assert
    expect(component.showScrollToBottom).toBeTrue();

    // Act
    component.onScrollChange(false);

    // Assert
    expect(component.showScrollToBottom).toBeFalse();
  });

  // Test di Integrazione
  it('Verifica che, alla chiamata del metodo onSendMessage di ChatContainerComponent, venga inviato un messaggio, '
    + 'venga impostato isLoading a true e venga recepita la risposta del bot proveniente da ChatService', fakeAsync(() => {
    // Arrange
    chatServiceSpy.sendMessage.and.returnValue(
      of({ response: 'RispostaBot' }).pipe(delay(50))
    );

    // Act
    component.onSendMessage('Ciao');

    // Assert
    expect(component.messages[0].text).toBe('Ciao');
    expect(component.isLoading).toBeTrue();
    tick(50);
    expect(component.messages[1].text.toString()).toContain('RispostaBot');
    expect(component.isLoading).toBeFalse();
  }));

  // Test di Unità
  it('Verifica che, alla chiamata del metodo onSendMessage di ChatContainerComponent venga ignorato l’invio di messaggi vuoti', () => {
    // Act
    component.onSendMessage('   ');

    // Assert
    expect(component.messages.length).toBe(0);
  });

  // Test di Integrazione
  it('Verifica che, alla chiamata del metodo onSendMessage di ChatContainerComponent, se ChatService segnala' +
    'un errore di rete, venga stampando un messaggio di errore', fakeAsync(() => {
    // Arrange
    chatServiceSpy.sendMessage.and.returnValue(
      new Observable(subscriber => {
        subscriber.error('Errore di rete');
      })
    );

    // Act
    component.onSendMessage('Test');

    // Assert
    tick();
    expect(component.messages[1].text).toBe('C’è stato un errore!');
    expect(component.isLoading).toBeFalse();
  }));

  // Test di Unità
  it('Verifica che, alla chiamata dell’evento onSuggestionClicked di ChatContainerComponent, venga inoltrato correttamente il ' +
    'suggerimento corrispondente al metodo onSendMessage', () => {
    // Arrange
    spyOn(component, 'onSendMessage');

    // Act
    component.onSuggestionClicked('Suggerimento');

    // Assert
    expect(component.onSendMessage).toHaveBeenCalledWith('Suggerimento');
  });
});
