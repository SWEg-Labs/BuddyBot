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
    // Arrange
    chatServiceSpy = jasmine.createSpyObj<ChatService>(
      'ChatService',
      [
        'sendMessage',
        'getLastMessageTimestamp',
        'getContinuationSuggestions',
        'checkFileUpdates',
        'setLastMessageTimestamp',
        'loadLastLoadOutcome'
      ]
    );
    chatServiceSpy.isUpdated$ = of(true);
    chatServiceSpy.getLastMessageTimestamp.and.returnValue(Date.now());
    chatServiceSpy.getContinuationSuggestions.and.returnValue(
      of({ "Cont1": "Come stai?", "Cont2": "Hai altre domande?" })
    );

    await TestBed.configureTestingModule({
      imports: [ChatContainerComponent],
      providers: [{ provide: ChatService, useValue: chatServiceSpy }]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================

  it('Dovrebbe creare correttamente un’istanza di ChatContainerComponent (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il componente ChatContainerComponent venga
     * creato correttamente, assicurandoci che l'istanza sia definita.
     */

    // AAA: Arrange
    // (Fase di arrangiamento già eseguita nel beforeEach)

    // AAA: Act
    // (Nessuna azione specifica)

    // AAA: Assert
    expect(component).toBeTruthy();
  });

  it('Dovrebbe impostare showScrollToBottom correttamente quando viene emesso l’evento onScrollChange (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il componente gestisca correttamente
     * il valore di showScrollToBottom al variare dell'evento di scroll.
     */

    // AAA: Arrange

    // AAA: Act
    component.onScrollChange(true);

    // AAA: Assert
    expect(component.showScrollToBottom).toBeTrue();

    // AAA: Act
    component.onScrollChange(false);

    // AAA: Assert
    expect(component.showScrollToBottom).toBeFalse();
  });

  it('Dovrebbe ignorare l’invio di messaggi vuoti (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che l'invio di un messaggio vuoto o composto
     * solo da spazi venga ignorato.
     */

    // AAA: Arrange

    // AAA: Act
    component.onSendMessage('   ');

    // AAA: Assert
    expect(component.messages.length).toBe(0);
  });

  it('Dovrebbe inoltrare correttamente il suggerimento cliccato (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il metodo onSuggestionClicked() inoltri
     * correttamente al metodo onSendMessage() il testo del suggerimento cliccato.
     */

    // AAA: Arrange
    spyOn(component, 'onSendMessage');

    // AAA: Act
    component.onSuggestionClicked('Suggerimento');

    // AAA: Assert
    expect(component.onSendMessage).toHaveBeenCalledWith('Suggerimento');
  });

  it('Dovrebbe impostare hideSuggestions a true quando si invia un messaggio e ripristinarlo a false alla risposta (Unit Test) - AAA', fakeAsync(() => {
    /**
     * In questo test verifichiamo che la proprietà hideSuggestions venga impostata a true
     * durante l'attesa della risposta e che torni a false una volta ricevuta la risposta.
     */

    // AAA: Arrange
    chatServiceSpy.sendMessage.and.returnValue(of({ response: 'Ok' }).pipe(delay(1)));

    // AAA: Act
    component.onSendMessage('Test');

    // AAA: Assert (dopo l'Act iniziale)
    expect(component.hideSuggestions).toBeTrue();

    tick(1);

    // AAA: Assert (dopo la risposta asincrona)
    expect(component.hideSuggestions).toBeFalse();
  }));

  // ==============================================================================
  //                              TEST DI INTEGRAZIONE
  // ==============================================================================

  it('Dovrebbe inviare un messaggio e ricevere la risposta dal bot (Integration Test) - AAA', fakeAsync(() => {
    /**
     * In questo test di integrazione verifichiamo la comunicazione con il servizio ChatService:
     * - il messaggio viene inviato
     * - viene restituita una risposta dal bot
     * - la risposta è gestita correttamente dal componente
     */

    // AAA: Arrange
    chatServiceSpy.sendMessage.and.returnValue(of({ response: 'RispostaBot' }).pipe(delay(50)));

    // AAA: Act
    component.onSendMessage('Ciao');

    // AAA: Assert (intermedio)
    expect(component.messages[0].content).toBe('Ciao');
    expect(component.isLoading).toBeTrue();

    tick(50);

    // AAA: Assert (finale)
    expect(component.messages[1].content.toString()).toContain('RispostaBot');
    expect(component.isLoading).toBeFalse();
  }));

  it('Dovrebbe gestire l’errore di rete quando si invia un messaggio (Integration Test) - AAA', fakeAsync(() => {
    /**
     * In questo test di integrazione verifichiamo che il componente gestisca correttamente
     * un eventuale errore di rete nella chiamata al servizio ChatService.
     */

    // AAA: Arrange
    chatServiceSpy.sendMessage.and.returnValue(
      new Observable(subscriber => {
        subscriber.error('Errore di rete');
      })
    );

    // AAA: Act
    component.onSendMessage('Test');
    tick();

    // AAA: Assert
    expect(component.messages[1].content).toBe('C’è stato un errore!');
    expect(component.isLoading).toBeFalse();
  }));
});
