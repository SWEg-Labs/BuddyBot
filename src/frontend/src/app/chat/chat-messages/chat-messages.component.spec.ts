import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ChatMessagesComponent } from './chat-messages.component';
import { Message, MessageSender } from '../../models/message.model';
import { By } from '@angular/platform-browser';

describe('ChatMessagesComponent', () => {
  let component: ChatMessagesComponent;
  let fixture: ComponentFixture<ChatMessagesComponent>;

  beforeEach(async () => {
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [ChatMessagesComponent],
    }).compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(ChatMessagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });


  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------

  describe('Test di unità', () => {
    it("Verifica che il componente ChatMessagesComponent venga creato", () => {
      // Act & Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che l'istanza del componente ChatMessagesComponent sia definita", () => {
      // Arrange:
      const localComponent = new ChatMessagesComponent();
      // Act & Assert:
      expect(localComponent).toBeDefined();
    });

    it("Verifica che il metodo onScroll di ChatMessagesComponent emetta true se non si è in fondo", () => {
      // Arrange:
      const fakeEl = { scrollHeight: 200, scrollTop: 30, clientHeight: 150 }; // distance = 20, isAtBottom = false
      Object.defineProperty(component, 'messagesContainer', { value: { nativeElement: fakeEl } });
      let emittedValue: boolean | undefined;
      component.isScrolledUp.subscribe(val => emittedValue = val);
      // Act:
      component.onScroll();
      // Assert:
      expect(emittedValue).toBeTrue();
    });

    it("Verifica che onScroll di ChatMessagesComponent emetta false se si è in fondo", () => {
      // Arrange:
      const fakeEl = { scrollHeight: 200, scrollTop: 150, clientHeight: 50 }; // distance = 0, isAtBottom = true
      Object.defineProperty(component, 'messagesContainer', { value: { nativeElement: fakeEl } });
      let emittedValue: boolean | undefined;
      component.isScrolledUp.subscribe(val => emittedValue = val);
      // Act:
      component.onScroll();
      // Assert:
      expect(emittedValue).toBeFalse();
    });

    it("Verifica che il metodo scrollToBottom di ChatMessagesComponent imposti scrollTop (la posizione di scorrimento verticale " +
      "corrente) uguale a scrollHeight (l'altezza totale del contenuto dell'elemento HTML)", () => {
      // Arrange:
      const fakeEl = { scrollHeight: 250, scrollTop: 0 };
      Object.defineProperty(component, 'messagesContainer', { value: { nativeElement: fakeEl } });
      // Act:
      component.scrollToBottom();
      // Assert:
      expect(fakeEl.scrollTop).toBe(250);
    });

    it("Verifica che il metodo onScroll di ChatMessagesComponent non fallisca se l'attributo messagesContainer è undefined", () => {
      // Arrange:
      Object.defineProperty(component, 'messagesContainer', { value: undefined });
      // Act & Assert:
      expect(() => component.onScroll()).not.toThrow();
    });

    it("Verifica che il metodo scrollToBottom di ChatMessagesComponent non fallisca se l'attributo messagesContainer è undefined", () => {
      // Arrange:
      Object.defineProperty(component, 'messagesContainer', { value: undefined });
      // Act & Assert:
      expect(() => component.scrollToBottom()).not.toThrow();
    });

    it("Verifica che l'evento ngAfterViewInit di ChatMessagesComponent aggiunga un event listener sull'attributo messagesContainer", () => {
      // Arrange:
      const fakeEl = document.createElement('div');
      spyOn(fakeEl, 'addEventListener').and.callThrough();
      Object.defineProperty(component, 'messagesContainer', { value: { nativeElement: fakeEl } });
      // Act:
      component.ngAfterViewInit();
      // Assert:
      expect(fakeEl.addEventListener).toHaveBeenCalledWith('click', jasmine.any(Function));
    });

    it("Verifica che il click sull'elemento HTML con classe CSS 'copy-snippet-icon' di ChatMessagesComponent chiami " +
      "il metodo copySnippet", () => {
      // Arrange:
      const container = document.createElement('div');
      container.classList.add('code-container');
      
      const copyIcon = document.createElement('span');
      copyIcon.classList.add('copy-snippet-icon');
      
      const snippetContent = document.createElement('div');
      snippetContent.classList.add('snippet-content');
      snippetContent.innerText = 'sample code';
      
      container.appendChild(copyIcon);
      container.appendChild(snippetContent);
      
      const fakeEl = document.createElement('div');
      fakeEl.appendChild(container);
      Object.defineProperty(component, 'messagesContainer', { value: { nativeElement: fakeEl } });
      
      const spyCopySnippet = spyOn<any>(component, 'copySnippet').and.callThrough();

      // Act:
      component.ngAfterViewInit();
      copyIcon.dispatchEvent(new MouseEvent('click', { bubbles: true }));

      // Assert:
      expect(spyCopySnippet).toHaveBeenCalledWith('sample code', copyIcon);
    });

    it("Verifica che stripHtml di ChatMessagesComponent converta correttamente l'HTML in testo", () => {
      // Arrange:
      const htmlString = "<div>Hello <strong>World</strong></div>";
      // Act:
      const result = (component as any).stripHtml(htmlString);
      // Assert:
      expect(result).toContain("Hello");
      expect(result).toContain("World");
    });

    it("Verifica che il metodo stripHtml di ChatMessagesComponent ritorni una stringa vuota se il parametro in input è vuoto", () => {
      // Arrange:
      const htmlString = "";
      // Act:
      const result = (component as any).stripHtml(htmlString);
      // Assert:
      expect(result).toBe("");
    });

    it("Verifica che il metodo copyToClipboard di ChatMessagesComponent rimuova 'content_copy' multiplo e modifichi " +
      "msg.copied", fakeAsync(() => {
      // Arrange:
      const msg: Message = new Message('content_copy some text content_copy', new Date(), MessageSender.CHATBOT);
      msg.copied = false;
      const writeTextSpy = spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());
      // Act:
      component.copyToClipboard(msg);
      tick(0);
      // Assert:
      const calledArg = (writeTextSpy.calls.mostRecent().args[0] as string);
      expect(calledArg.includes('content_copy')).toBeFalse();
      expect(msg.copied).toBeTrue();
      tick(1000);
      expect(msg.copied).toBeFalse();
    }));

    it("Verifica che il metodo copyToClipboard di ChatMessagesComponent usi l'attributo msg.sanitizedContent " +
      "del parametro msg se disponibile", fakeAsync(() => {
      // Arrange:
      const msg: Message = new Message('Fallback text', new Date(), MessageSender.CHATBOT);
      (msg as any).sanitizedContent = "Sanitized <br> text";
      msg.copied = false;
      const writeTextSpy = spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());
      // Act:
      component.copyToClipboard(msg);
      tick(0);
      // Assert:
      const calledArg = (writeTextSpy.calls.mostRecent().args[0] as string);
      expect(calledArg).toContain("Sanitized");
      tick(1000);
    }));

    it("Verifica che il metodo copySnippet di ChatMessagesComponent chiami il metodo navigator.clipboard.writeText e " +
      "inserisca e poi rimuova opportunamente la classe CSS 'snippet-copied' all'icona di copia", fakeAsync(() => {
      // Arrange:
      const fakeIcon = document.createElement('span');
      fakeIcon.classList.add('copy-snippet-icon');
      spyOn(navigator.clipboard, 'writeText').and.returnValue(Promise.resolve());
      spyOn(fakeIcon.classList, 'add').and.callThrough();
      spyOn(fakeIcon.classList, 'remove').and.callThrough();
      // Act:
      (component as any).copySnippet('sample snippet', fakeIcon);
      tick(0);
      // Assert:
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('sample snippet');
      expect(fakeIcon.classList.add).toHaveBeenCalledWith('snippet-copied');
      tick(1000);
      expect(fakeIcon.classList.remove).toHaveBeenCalledWith('snippet-copied');
    }));
  });
});
