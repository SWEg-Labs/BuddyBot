import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatBadgeComponent } from './chat-badge.component';
import { ChatService } from '../chat.service';
import { of } from 'rxjs';

describe('ChatBadgeComponent', () => {
  let component: ChatBadgeComponent;
  let fixture: ComponentFixture<ChatBadgeComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    chatServiceSpy = jasmine.createSpyObj('ChatService', ['checkFileUpdates'], {
    });

    await TestBed.configureTestingModule({
      imports: [ChatBadgeComponent],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    chatServiceSpy.isUpdated$ = of(true);
    fixture = TestBed.createComponent(ChatBadgeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // Test di Unità
  it('Verifica che venga creata correttamente un’istanza di ChatBadgeComponent', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('Verifica che isUpdated di ChatBadgeComponent venga impostato inizialmente al valore true', () => {
    // Assert
    expect(component.isUpdated).toBeTrue();

  });

  // Test di Unità
  it('Verifica che onToggleStatus() di ChatBadgeComponent chiami checkFileUpdates() di chatServiceSpy', () => {
    // Act
    component.onToggleStatus();

    // Assert
    expect(chatServiceSpy.checkFileUpdates).toHaveBeenCalled();
  });

  // Test di Unità
  it('Verifica che, al cambio di valore di isUpdated$ di chatServiceSpy, isUpdated di ChatBadgeComponent si aggiorni ' +
    'correttamente', () => {
    // Arrange
    chatServiceSpy.isUpdated$ = of(false);
    fixture = TestBed.createComponent(ChatBadgeComponent);
    component = fixture.componentInstance;

    // Act
    fixture.detectChanges();

    // Assert
    expect(component.isUpdated).toBeFalse();
  });
});
