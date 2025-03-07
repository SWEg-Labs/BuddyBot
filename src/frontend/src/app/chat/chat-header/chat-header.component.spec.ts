import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatHeaderComponent } from './chat-header.component';
import { ChatService } from '../chat.service';
import { of } from 'rxjs';

describe('ChatHeaderComponent', () => {
  let component: ChatHeaderComponent;
  let fixture: ComponentFixture<ChatHeaderComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
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
    fixture = TestBed.createComponent(ChatHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // Test di Unità
  it('Verifica che venga creata correttamente un’istanza di ChatHeaderComponent', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('Verifica che ChatHeaderComponent contenga il badge di aggiornamento nel proprio template HTML', () => {
    // Assert
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('app-chat-badge')).toBeTruthy();
  });
});
