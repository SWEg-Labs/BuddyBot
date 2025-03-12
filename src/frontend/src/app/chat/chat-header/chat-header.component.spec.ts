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
    chatServiceSpy = jasmine.createSpyObj('ChatService', ['checkFileUpdates'], {
      isUpdated$: of(true)
    });

    await TestBed.configureTestingModule({
      imports: [ChatHeaderComponent],
      providers: [{ provide: ChatService, useValue: chatServiceSpy }]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatHeaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================
  
  it('Dovrebbe creare correttamente un’istanza di ChatHeaderComponent (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che il componente ChatHeaderComponent venga
     * creato correttamente e che l'istanza sia definita.
     */

    // AAA: Arrange
    // (Fatto nel beforeEach)

    // AAA: Act
    // (Nessuna azione specifica)

    // AAA: Assert
    expect(component).toBeTruthy();
  });

  it('Dovrebbe contenere il badge di aggiornamento nel template HTML (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che nel template HTML del componente
     * sia presente l'elemento <app-chat-badge>.
     */

    // AAA: Arrange
    const compiled = fixture.nativeElement as HTMLElement;

    // AAA: Act
    // (Nessuna azione specifica, semplicemente ispezioniamo il DOM)

    // AAA: Assert
    expect(compiled.querySelector('app-chat-badge')).toBeTruthy();
  });
});
