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
  // Test di unità
  // ------------------------------------------------------

  describe('Test di unità', () => {
    it("Verifica che il componente ChatInputComponent venga creato", () => {
      // Act & Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che la barra di input di ChatInputContainer abbia il placeholder " +
      "'Scrivi un messaggio...'", () => {
      // Act:
      const input = fixture.nativeElement.querySelector('input');
      // Assert:
      expect(input.placeholder).toBe('Scrivi un messaggio...');
    });

    it("Verifica che la barra di input di ChatInputComponent sia disabilitata se l'attributo isLoading è true", async () => {
      // Arrange:
      component.isLoading = true;
      fixture.detectChanges();
      await fixture.whenStable();
      // Act:
      const input = fixture.nativeElement.querySelector('input');
      // Assert
      expect(input.getAttribute('disabled')).not.toBeNull();
    });

    it("Verifica che la barra di input di ChatInputComponent non sia disabilitata se l'attributo isLoading è false", () => {
      // Arrange:
      component.isLoading = false;
      fixture.detectChanges();
      // Act:
      const input = fixture.nativeElement.querySelector('input');
      // Assert:
      expect(input.disabled).toBeFalse();
    });

    it("Verifica che, quando si digita nella barra di input di ChatInputComponent, il valore dell'attributo userInput si aggiorni", () => {
      // Arrange:
      const input = fixture.debugElement.query(By.css('input')).nativeElement;
      // Act:
      input.value = 'Nuovo messaggio';
      input.dispatchEvent(new Event('input'));
      fixture.detectChanges();
      // Assert:
      expect(component.userInput).toBe('Nuovo messaggio');
    });

    it("Verifica che il bottone 'Invia' di ChatInputComponent sia disabilitato se l'attributo isLoading è true", () => {
      // Arrange:
      component.isLoading = true;
      fixture.detectChanges();
      // Act:
      const button = fixture.nativeElement.querySelector('button');
      // Assert:
      expect(button.disabled).toBeTrue();
    });

    it("Verifica che il bottone 'Invia' di ChatInputComponent sia disabilitato se l'attributo userInput è vuoto", () => {
      // Arrange:
      component.isLoading = false;
      component.userInput = '';
      fixture.detectChanges();
      // Act:
      const button = fixture.nativeElement.querySelector('button');
      // Assert:
      expect(button.disabled).toBeTrue();
    });

    it("Verifica che il bottone 'Invia' di ChatInputComponent sia disabilitato se l'attributo userInput contiene solo spazi", () => {
      // Arrange:
      component.isLoading = false;
      component.userInput = '    ';
      fixture.detectChanges();
      // Act:
      const button = fixture.nativeElement.querySelector('button');
      // Assert:
      expect(button.disabled).toBeTrue();
    });

    it("Verifica che il bottone 'Invia' di ChatInputComponent sia abilitato se l'attributo isLoading è false e userInput contiene " +
      "un messaggio valido", () => {
      // Arrange:
      component.isLoading = false;
      component.userInput = 'Test';
      fixture.detectChanges();
      // Act:
      const button = fixture.nativeElement.querySelector('button');
      // Assert:
      expect(button.disabled).toBeFalse();
    });

    it("Verifica che, quando si clicca il bottone 'Invia' di ChatInputComponent, venga inviata la stringa corretta", () => {
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

    it("Verifica che, quando si preme il tasto Enter e il focus sta nella barra di input di ChatInputComponent, venga inviata " +
      "la stringa corretta", () => {
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

    it("Verifica che il metodo onSend di ChatInputComponent non emetta alcun segnale se l'input dell'utente è vuoto " +
      "oppure contiene solo spazi", () => {
      // Arrange:
      spyOn(component.sendMessage, 'emit');
      component.userInput = '   ';
      // Act:
      component.onSend();
      // Assert:
      expect(component.sendMessage.emit).not.toHaveBeenCalled();
    });

    it("Verifica che il metodo onSend di ChatInputComponent non emetta alcun segnale se isLoading è true", () => {
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

    it("Verifica che il metodo onSend di ChatInputComponent emetta il valore corretto e resetti l'input dell'utente se le condizioni " +
      "di invio della domanda sono soddisfatte, cioè userInput contenga dei caratteri e isLoading sia false", () => {
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
