import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatHeaderComponent } from './chat-header.component';
import { ChatService } from '../chat.service';
import { of } from 'rxjs';

describe('ChatHeaderComponent', () => {
  let component: ChatHeaderComponent;
  let fixture: ComponentFixture<ChatHeaderComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange
    chatServiceSpy = jasmine.createSpyObj('ChatService', [
      'checkFileUpdates'
    ], {
      isUpdated$: of(true)
    });

    await TestBed.configureTestingModule({
      imports: [ChatHeaderComponent],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    // Act
    fixture = TestBed.createComponent(ChatHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------- Unit -------------------
  it('should create the ChatHeaderComponent instance successfully', () => {
    // Assert
    expect(component).toBeTruthy();
  });
});
