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
    chatServiceSpy = jasmine.createSpyObj('ChatService', ['checkFileUpdates'], {});
    chatServiceSpy.isUpdated$ = of(true);

    await TestBed.configureTestingModule({
      imports: [ChatBadgeComponent],
      providers: [{ provide: ChatService, useValue: chatServiceSpy }]
    }).compileComponents();
  });

  beforeEach(() => {
    // Arrange
    fixture = TestBed.createComponent(ChatBadgeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================

  it('Dovrebbe creare correttamente un’istanza di ChatBadgeComponent (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo la creazione del componente ChatBadgeComponent,
     * assicurandoci che l'istanza sia definita.
     */

    // AAA: Arrange
    // (Fatto in beforeEach)

    // AAA: Act
    // (Nessuna azione ulteriore)

    // AAA: Assert
    expect(component).toBeTruthy();
  });

  it('Dovrebbe impostare isUpdated inizialmente a true (Unit Test) - AAA', () => {
    /**
     * In questo test controlliamo che la proprietà "isUpdated" 
     * sia inizialmente impostata a true.
     */

    // AAA: Arrange
    // (Fatto in beforeEach)

    // AAA: Act
    // (Nessuna azione specifica)

    // AAA: Assert
    expect(component.isUpdated).toBeTrue();
  });

  it('Dovrebbe chiamare checkFileUpdates quando viene invocato onToggleStatus (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che richiamando onToggleStatus() 
     * venga effettivamente invocato il metodo checkFileUpdates() del ChatService.
     */

    // AAA: Arrange

    // AAA: Act
    component.onToggleStatus();

    // AAA: Assert
    expect(chatServiceSpy.checkFileUpdates).toHaveBeenCalled();
  });

  it('Dovrebbe aggiornare isUpdated al cambiamento di isUpdated$ (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che la proprietà isUpdated venga aggiornata correttamente
     * quando il BehaviorSubject isUpdated$ emette un nuovo valore (false).
     */

    // AAA: Arrange
    chatServiceSpy.isUpdated$ = of(false);
    fixture = TestBed.createComponent(ChatBadgeComponent);
    component = fixture.componentInstance;

    // AAA: Act
    fixture.detectChanges();

    // AAA: Assert
    expect(component.isUpdated).toBeFalse();
  });
});
