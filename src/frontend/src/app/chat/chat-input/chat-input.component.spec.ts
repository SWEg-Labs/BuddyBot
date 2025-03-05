import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatInputComponent } from './chat-input.component';

describe('ChatInputComponent', () => {
  let component: ChatInputComponent;
  let fixture: ComponentFixture<ChatInputComponent>;

  beforeEach(async () => {
    // Arrange
    await TestBed.configureTestingModule({
      imports: [ ChatInputComponent ],
    }).compileComponents();
  });

  beforeEach(() => {
    // Act
    fixture = TestBed.createComponent(ChatInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------- Unit -------------------
  it('should create the ChatInputComponent instance successfully', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // ------------------- Unit -------------------
  it('should emit the sendMessage event when onSend() is invoked with valid input', () => {
    // Arrange
    spyOn(component.sendMessage, 'emit');
    component.userInput = 'Hello';

    // Act
    component.onSend();

    // Assert
    expect(component.sendMessage.emit).toHaveBeenCalledWith('Hello');
    expect(component.userInput).toBe(''); // reset dell’input
  });

  // ------------------- Unit -------------------
  it('should NOT emit the sendMessage event if isLoading is true', () => {
    // Arrange
    spyOn(component.sendMessage, 'emit');
    component.isLoading = true;
    component.userInput = 'Some text';

    // Act
    component.onSend();

    // Assert
    expect(component.sendMessage.emit).not.toHaveBeenCalled();
  });
});
