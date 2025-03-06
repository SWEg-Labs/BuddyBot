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
  it('deve creare correttamente l’istanza di ChatInputComponent', () => {
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('deve emettere l’evento sendMessage con il testo corretto se si preme Invio', () => {
    spyOn(component.sendMessage, 'emit');
    const input = fixture.debugElement.query(By.css('input')).nativeElement;
    input.value = 'Ciao';
    input.dispatchEvent(new Event('input'));
    input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));
    expect(component.sendMessage.emit).toHaveBeenCalledWith('Ciao');
  });

  // Test di Unità
  it('non deve emettere l’evento sendMessage se isLoading=true', () => {
    spyOn(component.sendMessage, 'emit');
    component.isLoading = true;
    component.userInput = 'Prova';
    component.onSend();
    expect(component.sendMessage.emit).not.toHaveBeenCalled();
  });

  // Test di Unità
  it('deve pulire il campo input dopo l’invio di un messaggio', () => {
    spyOn(component.sendMessage, 'emit');
    component.userInput = 'Messaggio';
    component.onSend();
    expect(component.userInput).toBe('');
  });
});
