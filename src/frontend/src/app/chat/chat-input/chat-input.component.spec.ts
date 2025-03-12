import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatInputComponent } from './chat-input.component';
import { FormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';

describe('ChatInputComponent', () => {
  let component: ChatInputComponent;
  let fixture: ComponentFixture<ChatInputComponent>;

  beforeEach(async () => {
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [ChatInputComponent, FormsModule],
    }).compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(ChatInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------------------------------------------
  // Test di integrazione
  // ------------------------------------------------------
  describe('Test di integrazione', () => {
    it("Verifica che il componente venga creato", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che il bottone 'Invia' sia disabilitato se isLoading è true", () => {
      // Arrange:
      component.isLoading = true;
      fixture.detectChanges();
      // Act:
      const button = fixture.nativeElement.querySelector('button');
      // Assert:
      expect(button.disabled).toBeTrue();
    });

    it("Verifica che il bottone 'Invia' sia abilitato se isLoading è false", () => {
      // Arrange:
      component.isLoading = false;
      fixture.detectChanges();
      // Act:
      const button = fixture.nativeElement.querySelector('button');
      // Assert:
      expect(button.disabled).toBeFalse();
    });

    it("Verifica che l'input abbia il placeholder 'Scrivi un messaggio...'", () => {
      // Arrange:
      // Act:
      const input = fixture.nativeElement.querySelector('input');
      // Assert:
      expect(input.placeholder).toBe('Scrivi un messaggio...');
    });

    it("Verifica che l'input sia disabilitato se isLoading è true", async () => {
      // Arrange:
      component.isLoading = true;
      fixture.detectChanges();
      await fixture.whenStable();
      // Act:
      const input = fixture.nativeElement.querySelector('input');
      // Assert (controllo dell'attributo 'disabled'):
      expect(input.getAttribute('disabled')).not.toBeNull();
    });
    

    it("Verifica che l'input non sia disabilitato se isLoading è false", () => {
      // Arrange:
      component.isLoading = false;
      fixture.detectChanges();
      // Act:
      const input = fixture.nativeElement.querySelector('input');
      // Assert:
      expect(input.disabled).toBeFalse();
    });

    it("Verifica che, quando si digita nell'input, il valore userInput si aggiorna", () => {
      // Arrange:
      const input = fixture.debugElement.query(By.css('input')).nativeElement;
      // Act:
      input.value = 'Nuovo messaggio';
      input.dispatchEvent(new Event('input'));
      fixture.detectChanges();
      // Assert:
      expect(component.userInput).toBe('Nuovo messaggio');
    });

    it("Verifica che, quando si clicca il bottone, venga inviata la stringa corretta", () => {
      // Arrange:
      spyOn(component.sendMessage, 'emit');
      component.isLoading = false;
      component.userInput = '  Test Message  ';
      fixture.detectChanges();
      // Act:
      const button = fixture.nativeElement.querySelector('button');
      button.click();
      // Assert:
      expect(component.sendMessage.emit).toHaveBeenCalledWith('Test Message');
      expect(component.userInput).toBe('');
    });

    it("Verifica che, quando si preme il tasto Enter nell'input, venga inviata la stringa corretta", () => {
      // Arrange:
      spyOn(component.sendMessage, 'emit');
      component.isLoading = false;
      component.userInput = 'Hello World';
      fixture.detectChanges();
      // Act:
      const inputEl = fixture.debugElement.query(By.css('input'));
      inputEl.triggerEventHandler('keyup.enter', {});
      // Assert:
      expect(component.sendMessage.emit).toHaveBeenCalledWith('Hello World');
      expect(component.userInput).toBe('');
    });
  });

  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------
  describe('Test di unità', () => {
    it("Verifica che onSend non emetta alcun valore se userInput è vuoto", () => {
      // Arrange:
      spyOn(component.sendMessage, 'emit');
      component.userInput = '   ';
      // Act:
      component.onSend();
      // Assert:
      expect(component.sendMessage.emit).not.toHaveBeenCalled();
    });

    it("Verifica che onSend non emetta alcun valore se isLoading è true", () => {
      // Arrange:
      spyOn(component.sendMessage, 'emit');
      component.userInput = 'Test';
      component.isLoading = true;
      // Act:
      component.onSend();
      // Assert:
      expect(component.sendMessage.emit).not.toHaveBeenCalled();
      expect(component.userInput).toBe('Test');
    });

    it("Verifica che onSend emetta il valore corretto e resetti userInput se le condizioni sono soddisfatte", () => {
      // Arrange:
      spyOn(component.sendMessage, 'emit');
      component.userInput = '  Example  ';
      component.isLoading = false;
      // Act:
      component.onSend();
      // Assert:
      expect(component.sendMessage.emit).toHaveBeenCalledWith('Example');
      expect(component.userInput).toBe('');
    });
  });
});
