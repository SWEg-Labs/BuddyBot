import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ChatMessagesComponent } from './chat-messages.component';
import { By } from '@angular/platform-browser';
import { Message, MessageSender } from '../../models/message.model';

describe('ChatMessagesComponent', () => {
  let component: ChatMessagesComponent;
  let fixture: ComponentFixture<ChatMessagesComponent>;

  beforeEach(async () => {
    // AAA: Arrange
    await TestBed.configureTestingModule({
      imports: [ChatMessagesComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    // AAA: Arrange
    fixture = TestBed.createComponent(ChatMessagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================

  it('Dovrebbe creare correttamente un’istanza di ChatMessagesComponent (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il componente ChatMessagesComponent venga
     * creato correttamente e l'istanza sia valida.
     */

    // AAA: Arrange
    // (Fatto nel beforeEach)

    // AAA: Act
    // (Nessuna azione specifica)

    // AAA: Assert
    expect(component).toBeTruthy();
  });

  it('Dovrebbe eseguire lo scroll fino al fondo della pagina quando viene chiamato scrollToBottom (Unit Test) - AAA', () => {
    /**
     * In questo test controlliamo che la funzione scrollToBottom
     * imposti scrollTop = scrollHeight, simulando lo scroll completo verso il basso.
     */

    // AAA: Arrange
    const mockScrollEl = {
      scrollHeight: 500,
      scrollTop: 0,
      clientHeight: 300
    };
    // Forziamo il riferimento interno all’elemento di scrolling
    (component as any).messagesContainer = { nativeElement: mockScrollEl };

    // AAA: Act
    component.scrollToBottom();

    // AAA: Assert
    expect(mockScrollEl.scrollTop).toBe(500);
  });

  it('Dovrebbe emettere isScrolledUp=true quando l’utente scorre lontano dal fondo (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che l’evento "isScrolledUp" emetta true
     * quando l'utente non è più "attaccato" al fondo del container.
     */

    // AAA: Arrange
    spyOn(component.isScrolledUp, 'emit');
    const mockScrollEl = {
      scrollHeight: 500,
      scrollTop: 10,
      clientHeight: 300
    };
    (component as any).messagesContainer = { nativeElement: mockScrollEl };

    // AAA: Act
    component.onScroll();

    // AAA: Assert
    expect(component.isScrolledUp.emit).toHaveBeenCalledWith(true);
  });

  it('Dovrebbe emettere isScrolledUp=false quando l’utente è vicino al fondo (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che l’evento "isScrolledUp" emetta false
     * quando l'utente si trova (o torna) vicino al fondo del container.
     */

    // AAA: Arrange
    spyOn(component.isScrolledUp, 'emit');
    const mockScrollEl = {
      scrollHeight: 500,
      scrollTop: 490, // a soli 10px dalla fine
      clientHeight: 300
    };
    (component as any).messagesContainer = { nativeElement: mockScrollEl };

    // AAA: Act
    component.onScroll();

    // AAA: Assert
    expect(component.isScrolledUp.emit).toHaveBeenCalledWith(false);
  });

  it('Dovrebbe mostrare il blocco di caricamento se isLoading=true (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il template visualizzi correttamente
     * il blocco di caricamento quando la proprietà isLoading è impostata a true.
     */

    // AAA: Arrange
    component.isLoading = true;

    // AAA: Act
    fixture.detectChanges();
    const loader = fixture.debugElement.query(By.css('app-chat-loading-indicator'));

    // AAA: Assert
    expect(loader).toBeTruthy();
  });

  it('Non dovrebbe mostrare il blocco di caricamento se isLoading=false (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il blocco di caricamento non sia presente
     * quando la proprietà isLoading è impostata a false.
     */

    // AAA: Arrange
    component.isLoading = false;

    // AAA: Act
    fixture.detectChanges();
    const loader = fixture.debugElement.query(By.css('app-chat-loading-indicator'));

    // AAA: Assert
    expect(loader).toBeFalsy();
  });

  it('Dovrebbe copiare l’intero messaggio negli appunti quando viene chiamato copyToClipboard (Unit Test) - AAA', async () => {
    /**
     * In questo test verifichiamo che la funzione copyToClipboard
     * copi correttamente negli appunti l’intero contenuto (senza HTML).
     */

    // AAA: Arrange
    const mockMessage: Message = {
      sender: MessageSender.CHATBOT,
      content: 'Testo <br> con <b>HTML</b>',
      timestamp: new Date()
    };
    spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());

    // AAA: Act
    await component.copyToClipboard(mockMessage);

    // AAA: Assert
    expect(mockMessage.copied).toBeTrue();
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('Testo \n con HTML');
  });

  it('Dovrebbe rimuovere la proprietà copied da un messaggio dopo 1 secondo (Unit Test) - AAA', fakeAsync(() => {
    /**
     * In questo test verifichiamo che la proprietà "copied"
     * venga disattivata (false) dopo 1 secondo dal momento della copia.
     */

    // AAA: Arrange
    const mockMessage: Message = {
      sender: MessageSender.CHATBOT,
      content: 'Messaggio di test',
      timestamp: new Date(),
      copied: false
    };
    spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());

    // AAA: Act
    component.copyToClipboard(mockMessage);
    tick(100);  // passano 100ms => copied è ancora true
    expect(mockMessage.copied).toBeTrue();
    tick(1000); // passano altri 900ms (totale 1s)
    // AAA: Assert
    expect(mockMessage.copied).toBeFalse();
  }));

  it('Dovrebbe evidenziare il pulsante di copia dello snippet quando viene chiamato copySnippet (Unit Test) - AAA', async () => {
    /**
     * In questo test verifichiamo che il metodo privato copySnippet 
     * aggiunga e poi rimuova la classe "snippet-copied" sull'icona di copia.
     */

    // AAA: Arrange
    spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());
    fixture.detectChanges();
    const iconElement = document.createElement('i');

    // AAA: Act
    // @ts-expect-error: accediamo al metodo privato per il test
    await component.copySnippet('codice di prova', iconElement);

    // AAA: Assert
    expect(iconElement.classList).toContain('snippet-copied');
  });

  // ==============================================================================
  //                              TEST DI INTEGRAZIONE
  // ==============================================================================
  
  it('Dovrebbe renderizzare correttamente i messaggi in arrivo (Integration Test) - AAA', () => {
    /**
     * In questo test di integrazione verifichiamo che i messaggi passati come input
     * vengano correttamente mostrati nel template HTML.
     */

    // AAA: Arrange
    component.messages = [
      new Message('Ciao', new Date('2023-10-01T10:00:00'), MessageSender.USER),
      new Message('Salve, come posso aiutarti?', new Date('2023-10-01T10:00:05'), MessageSender.CHATBOT),
    ];

    // AAA: Act
    fixture.detectChanges();
    const messageEls = fixture.debugElement.queryAll(By.css('.message'));

    // AAA: Assert
    expect(messageEls.length).toBe(2);
    // Primo messaggio: deve essere 'user-message'
    expect(messageEls[0].nativeElement.classList).toContain('user-message');
    // Secondo messaggio: deve essere 'bot-message'
    expect(messageEls[1].nativeElement.classList).toContain('bot-message');
  });

  it('Dovrebbe catturare il click sulle icone "copy-snippet-icon" e chiamare copySnippet (Integration Test) - AAA', () => {
    /**
     * In questo test di integrazione verifichiamo il comportamento reale
     * dell'evento click sull'icona di copia di un blocco di codice:
     * - Inseriamo un messaggio che simuli un blocco di codice
     * - Simuliamo il click sul pulsante di copia
     * - Verifichiamo che la funzione copySnippet sia stata chiamata
     */

    // AAA: Arrange
    spyOn<any>(component, 'copySnippet').and.callThrough();
    component.messages = [
      new Message(
        'Esempio di codice:\n```ts\nconsole.log("Hello!");\n```',
        new Date(),
        MessageSender.CHATBOT
      )
    ];

    // AAA: Act
    fixture.detectChanges();
    const snippetIcon = fixture.debugElement.query(By.css('.copy-snippet-icon'));
    snippetIcon.nativeElement.click();

    // AAA: Assert
    expect(component['copySnippet']).toHaveBeenCalled();
  });

});
