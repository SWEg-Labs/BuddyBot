import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatMessagesComponent } from './chat-messages.component';

describe('ChatMessagesComponent', () => {
  let component: ChatMessagesComponent;
  let fixture: ComponentFixture<ChatMessagesComponent>;

  beforeEach(async () => {
    // Arrange
    await TestBed.configureTestingModule({
      imports: [ ChatMessagesComponent ],
    }).compileComponents();
  });

  beforeEach(() => {
    // Act
    fixture = TestBed.createComponent(ChatMessagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------- Unit -------------------
  it('should create the ChatMessagesComponent instance successfully', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // ------------------- Unit -------------------
  it('should scroll to the bottom when scrollToBottom() is called', () => {
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

  // ------------------- Unit -------------------
  it('should emit isScrolledUp=true when the user scrolls away from the bottom', () => {
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
});
