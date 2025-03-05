import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ChatContainerComponent } from './chat-container.component';
import { ChatService } from '../chat.service';
import { of } from 'rxjs';
import { delay } from 'rxjs/operators';

describe('ChatContainerComponent', () => {
  let component: ChatContainerComponent;
  let fixture: ComponentFixture<ChatContainerComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange
    chatServiceSpy = jasmine.createSpyObj('ChatService', [
      'sendMessage',
      'getLastMessageTimestamp',
      'getContinuationSuggestions',
      'getInitialSuggestions',
      'checkFileUpdates'
    ], {
      isUpdated$: of(true)
    });

    chatServiceSpy.getInitialSuggestions.and.returnValue(of(['Ini1', 'Ini2']));
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of(['Cont1', 'Cont2']));

    await TestBed.configureTestingModule({
      imports: [ChatContainerComponent],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    // Act
    fixture = TestBed.createComponent(ChatContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------- Unit -------------------
  it('should create the ChatContainerComponent instance successfully', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // -------------- Integration -----------------
  it('should set isLoading to true while sending a message, then false once the response arrives', fakeAsync(() => {
    // Arrange
    chatServiceSpy.sendMessage.and.returnValue(
      of({ response: 'Ok' }).pipe(delay(1))
    );

    // Act
    component.onSendMessage('Ciao');

    // Assert (subito dopo la chiamata)
    expect(component.isLoading).toBeTrue();

    // Avanziamo il tempo simulando la risposta
    tick(1);
    fixture.detectChanges();
    expect(component.isLoading).toBeFalse();
  }));

  // -------------- Integration -----------------
  it('should call chatService.sendMessage() and update messages appropriately', fakeAsync(() => {
    // Arrange
    chatServiceSpy.sendMessage.and.returnValue(
      of({ response: 'Hello from server' }).pipe(delay(1))
    );

    // Act
    component.onSendMessage('Test');
    fixture.detectChanges();

    // Assert (prima della risposta)
    expect(component.isLoading).toBeTrue();

    // Avanza il tempo simulando la risposta
    tick(1);
    fixture.detectChanges();

    // Ora isLoading dev'essere false
    expect(component.isLoading).toBeFalse();

    // Verifica che ChatService sia stato chiamato
    expect(chatServiceSpy.sendMessage).toHaveBeenCalledWith('Test');
    // Verifica che i messaggi siano 2 (Utente + Bot)
    expect(component.messages.length).toBe(2);
    const botMsg = String(component.messages[1].text);
    expect(botMsg).toContain('Hello from server');
  }));
});
