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
  it('deve creare correttamente l’istanza di ChatBadgeComponent', () => {
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('deve impostare isUpdated quando cambia la variabile in ChatService', () => {
    expect(component.isUpdated).toBeTrue();
  });

  // Test di Unità
  it('deve chiamare checkFileUpdates() in onToggleStatus()', () => {
    component.onToggleStatus();
    expect(chatServiceSpy.checkFileUpdates).toHaveBeenCalled();
  });

  // Test di Unità
  it('deve cambiare isUpdated al cambio di valore in isUpdated$', () => {
    chatServiceSpy.isUpdated$ = of(false);
    fixture = TestBed.createComponent(ChatBadgeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    expect(component.isUpdated).toBeFalse();
  });
});
