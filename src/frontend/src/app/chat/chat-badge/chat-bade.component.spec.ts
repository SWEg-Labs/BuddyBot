import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatBadgeComponent } from './chat-badge.component';
import { ChatService } from '../chat.service';
import { of } from 'rxjs';

describe('ChatBadgeComponent', () => {
  let component: ChatBadgeComponent;
  let fixture: ComponentFixture<ChatBadgeComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange
    chatServiceSpy = jasmine.createSpyObj('ChatService', ['checkFileUpdates'], {
      isUpdated$: of(true)
    });

    await TestBed.configureTestingModule({
      imports: [ChatBadgeComponent],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    // Act
    fixture = TestBed.createComponent(ChatBadgeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------- Unit -------------------
  it('should create the ChatBadgeComponent instance successfully', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // -------------- Integration -----------------
  it('should call chatService.checkFileUpdates() when onToggleStatus() is invoked', () => {
    // Arrange

    // Act
    component.onToggleStatus();

    // Assert
    expect(chatServiceSpy.checkFileUpdates).toHaveBeenCalled();
  });
});
