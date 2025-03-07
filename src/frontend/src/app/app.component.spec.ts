import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { ChatService } from './chat/chat.service';
import { of } from 'rxjs';

describe('AppComponent', () => {
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange
    chatServiceSpy = jasmine.createSpyObj('ChatService', [
      'sendMessage',
      'getLastMessageTimestamp',
      'getContinuationSuggestions',
      'getInitialSuggestions',
      'checkFileUpdates',
    ], {
      isUpdated$: of(true)
    });

    chatServiceSpy.getInitialSuggestions.and.returnValue(of(['Ini1', 'Ini2']));
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of(['Cont1', 'Cont2']));

    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  // Test di Unità
  it('Verifica che venga creata correttamente un’istanza di AppComponent', () => {
    // Act
    const fixture = TestBed.createComponent(AppComponent);

    // Assert
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
});
