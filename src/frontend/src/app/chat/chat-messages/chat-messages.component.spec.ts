import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatMessagesComponent } from './chat-messages.component';
import { Message } from '../../models/message.model';
import { By } from '@angular/platform-browser';

describe('ChatMessagesComponent', () => {
  let component: ChatMessagesComponent;
  let fixture: ComponentFixture<ChatMessagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ ChatMessagesComponent ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatMessagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // Test di Unità
  it('Verifica che venga creata correttamente un’istanza di ChatMessagesComponent', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('Verifica che, alla chiamata del metodo scrollToBottom di ChatMessagesComponent, venga eseguito lo scroll fino al fondo ' +
    'della pagina', () => {
    // Arrange
    const mockScrollEl = {
      scrollHeight: 500,
      scrollTop: 0,
      clientHeight: 300
    };
    (component as any).messagesContainer = { nativeElement: mockScrollEl };

    // Act
    component.scrollToBottom();

    // Assert
    expect(mockScrollEl.scrollTop).toBe(500);
  });

  // Test di Unità
  it('Verifica che, quando l’utente scorre lontano dal fondo della pagina, venga emesso l’evento isScrolledUp di '+
    'ChatMessagesComponent a valore true ', () => {
    // Arrange
    spyOn(component.isScrolledUp, 'emit');
    const mockScrollEl = {
      scrollHeight: 500,
      scrollTop: 10,
      clientHeight: 300
    };
    (component as any).messagesContainer = { nativeElement: mockScrollEl };

    // Act
    component.onScroll();

    // Assert
    expect(component.isScrolledUp.emit).toHaveBeenCalledWith(true);
  });

  // Test di Unità
  it('Verifica che, alla chiamata del metodo copyToClipboard di ChatMessagesComponent, venga copiato l’intero messaggio '+
    'negli appunti', async () => {
    // Arrange
    const mockMessage: Message = { sender: 'Bot', text: 'Testo <br> con <b>HTML</b>' };
    spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());

    // Act
    await component.copyToClipboard(mockMessage);

    // Assert
    expect(mockMessage.copied).toBeTrue();
  });

  // Test di Unità
  it('Verifica che, alla chiamata del metodo copySnippet di ChatMessagesComponent, venga evidenziato il pulsante di copia ' +
    'dello snippet', async () => {
    // Arrange
    spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());
    fixture.detectChanges();
    const iconElement = document.createElement('i');

    // Act
    await component['copySnippet']('codice di prova', iconElement);

    // Assert
    expect(iconElement.classList).toContain('snippet-copied');
  });

  // Test di Integrazione
  it('Verifica che, quando la variabile isLoading di ChatMessagesComponent vale true, venga mostrato il blocco '+
    'di caricamento di ChatLoadingIndicatorComponent', () => {
    // Arrange
    component.isLoading = true;

    // Act
    fixture.detectChanges();

    // Assert
    const loader = fixture.debugElement.query(By.css('app-chat-loading-indicator'));
    expect(loader).toBeTruthy();
  });
});
