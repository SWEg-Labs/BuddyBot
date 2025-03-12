import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatLoadingIndicatorComponent } from './chat-loading-indicator.component';

describe('ChatLoadingIndicatorComponent', () => {
  let component: ChatLoadingIndicatorComponent;
  let fixture: ComponentFixture<ChatLoadingIndicatorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ ChatLoadingIndicatorComponent ]
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatLoadingIndicatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ==============================================================================
  //                              TEST DI UNITÀ
  // ==============================================================================

  it('Verifica che venga creata correttamente un’istanza di ChatLoadingIndicatorComponent (Unit Test) - AAA', () => {
    /**
     * In questo test controlliamo che il componente ChatLoadingIndicatorComponent
     * venga creato con successo.
     */

    // AAA: Arrange
    // (Nessuna disposizione speciale)

    // AAA: Act
    // (Nessuna azione necessaria)

    // AAA: Assert
    expect(component).toBeTruthy();
  });

  it('Verifica che il template HTML contenga un\'immagine con la classe rotating-logo (Unit Test) - AAA', () => {
    /**
     * In questo test verifichiamo che all'interno del template del componente
     * esista effettivamente l'immagine con classe "rotating-logo".
     */

    // AAA: Arrange
    const compiled = fixture.nativeElement as HTMLElement;

    // AAA: Act
    const img = compiled.querySelector('img.rotating-logo');

    // AAA: Assert
    expect(img).toBeTruthy();
  });
});
