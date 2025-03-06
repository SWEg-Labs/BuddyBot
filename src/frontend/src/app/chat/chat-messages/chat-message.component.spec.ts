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
  it('deve creare correttamente l’istanza di ChatMessagesComponent', () => {
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('deve eseguire lo scroll in fondo quando viene chiamato scrollToBottom()', () => {
    const mockScrollEl = {
      scrollHeight: 500,
      scrollTop: 0,
      clientHeight: 300
    };
    (component as any).messagesContainer = { nativeElement: mockScrollEl };
    component.scrollToBottom();
    expect(mockScrollEl.scrollTop).toBe(500);
  });

  // Test di Unità
  it('deve emettere isScrolledUp=true quando l’utente si scorre lontano dal fondo', () => {
    spyOn(component.isScrolledUp, 'emit');
    const mockScrollEl = {
      scrollHeight: 500,
      scrollTop: 10,
      clientHeight: 300
    };
    (component as any).messagesContainer = { nativeElement: mockScrollEl };
    component.onScroll();
    expect(component.isScrolledUp.emit).toHaveBeenCalledWith(true);
  });

  // Test di Unità
  it('deve copiare l’intero messaggio negli appunti quando viene chiamato copyToClipboard()', async () => {
    const mockMessage: Message = { sender: 'Bot', text: 'Testo <br> con <b>HTML</b>' };
    spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());
    await component.copyToClipboard(mockMessage);
    expect(mockMessage.copied).toBeTrue();
  });

  // Test di Unità
  it('deve evidenziare il pulsante di copia dello snippet quando viene chiamato copySnippet()', async () => {
    spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());
    fixture.detectChanges();
    const iconElement = document.createElement('i');
    await component['copySnippet']('codice di prova', iconElement);
    expect(iconElement.classList).toContain('snippet-copied');
  });

  // Test di Integrazione
  it('deve mostrare il componente di caricamento quando isLoading è true', () => {
    component.isLoading = true;
    fixture.detectChanges();
    const loader = fixture.debugElement.query(By.css('app-chat-loading-indicator'));
    expect(loader).toBeTruthy();
  });
});
