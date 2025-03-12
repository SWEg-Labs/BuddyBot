import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatInputComponent } from './chat-input.component';
import { By } from '@angular/platform-browser';

describe('ChatInputComponent', () => {
  let component: ChatInputComponent;
  let fixture: ComponentFixture<ChatInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ ChatInputComponent ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================

  it('Verifica che venga creata correttamente un’istanza di ChatInputComponent (Unit Test) - AAA', () => {
    /**
     * In questo test assicuriamo che il componente ChatInputComponent
     * sia creato correttamente.
     */

    // AAA: Arrange
    // (Fase di arrangiamento eseguita nel beforeEach)

    // AAA: Act
    // (Nessun atto particolare)

    // AAA: Assert
    expect(component).toBeTruthy();
  });

  it('Verifica che, se viene premuto Invio, venga emesso l’evento sendMessage di ChatInputComponent con il testo corretto (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il componente emetta correttamente
     * l'evento "sendMessage" quando l'utente preme Invio nell'input.
     */

    // AAA: Arrange
    spyOn(component.sendMessage, 'emit');
    const input = fixture.debugElement.query(By.css('input')).nativeElement;
    input.value = 'Ciao';

    // AAA: Act
    input.dispatchEvent(new Event('input'));
    input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));

    // AAA: Assert
    expect(component.sendMessage.emit).toHaveBeenCalledWith('Ciao');
  });

  it('Verifica che non sia possibile emettere l’evento sendMessage se isLoading=true (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che l'evento "sendMessage" non venga emesso
     * se la proprietà "isLoading" è impostata a true.
     */

    // AAA: Arrange
    spyOn(component.sendMessage, 'emit');
    component.isLoading = true;
    component.userInput = 'Prova';

    // AAA: Act
    component.onSend();

    // AAA: Assert
    expect(component.sendMessage.emit).not.toHaveBeenCalled();
  });

  it('Verifica che, dopo l’invio di un messaggio, il campo input venga pulito (Unit Test) - AAA', () => {
    /**
     * In questo test ci assicuriamo che il campo di input venga svuotato
     * dopo aver inviato correttamente un messaggio.
     */

    // AAA: Arrange
    spyOn(component.sendMessage, 'emit');
    component.userInput = 'Messaggio';

    // AAA: Act
    component.onSend();

    // AAA: Assert
    expect(component.userInput).toBe('');
  });
});
