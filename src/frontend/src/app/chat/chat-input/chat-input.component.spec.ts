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

  // Test di Unità
  it('Verifica che venga creata correttamente un’istanza di ChatInputComponent', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('Verifica che, se viene premuto Invio, venga emesso l’evento sendMessage di ChatInputComponent con il testo corretto', () => {
    spyOn(component.sendMessage, 'emit');
    // Arrange
    const input = fixture.debugElement.query(By.css('input')).nativeElement;
    input.value = 'Ciao';

    // Act
    input.dispatchEvent(new Event('input'));
    input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));

    // Assert
    expect(component.sendMessage.emit).toHaveBeenCalledWith('Ciao');
  });

  // Test di Unità
  it('Verifica che non sia possibile emettere l’evento sendMessage di ChatInputComponent se isLoading=true', () => {
    // Arrange
    spyOn(component.sendMessage, 'emit');
    component.isLoading = true;
    component.userInput = 'Prova';

    // Act
    component.onSend();

    // Arrange
    expect(component.sendMessage.emit).not.toHaveBeenCalled();
  });

  // Test di Unità
  it('Verifica che, dopo l’invio di un messaggio, il campo input di ChatInputComponent venga pulito', () => {
    // Arrange
    spyOn(component.sendMessage, 'emit');
    component.userInput = 'Messaggio';

    // Act
    component.onSend();

    // Assert
    expect(component.userInput).toBe('');
  });
});
