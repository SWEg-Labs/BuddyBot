import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { ChatService } from './chat/chat.service';
import { of } from 'rxjs';

describe('AppComponent', () => {
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange
    chatServiceSpy = jasmine.createSpyObj(
      'ChatService',
      [
        'sendMessage',
        'getLastMessageTimestamp',
        'getContinuationSuggestions',
        'getInitialSuggestions',
        'checkFileUpdates'
      ],
      {
        isUpdated$: of(true),
      }
    );

    chatServiceSpy.getContinuationSuggestions.and.returnValue(of({ cont1: 'Cont1', cont2: 'Cont2' } as Record<string, string>));

    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [{ provide: ChatService, useValue: chatServiceSpy }]
    }).compileComponents();
  });

  // TEST DI UNITÀ
  it('Dovrebbe creare correttamente un’istanza di AppComponent (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo la creazione del componente principale dell'applicazione,
     * assicurandoci che l'istanza di AppComponent sia definita.
     */

    // AAA: Arrange
    // (La fase di arrangiamento è stata fatta nel beforeEach)

    // AAA: Act
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    // AAA: Assert
    expect(app).toBeTruthy();
  });
});
