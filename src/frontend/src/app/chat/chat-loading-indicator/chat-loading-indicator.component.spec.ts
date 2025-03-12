import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatLoadingIndicatorComponent } from './chat-loading-indicator.component';

describe('ChatLoadingIndicatorComponent', () => {
  let component: ChatLoadingIndicatorComponent;
  let fixture: ComponentFixture<ChatLoadingIndicatorComponent>;

  beforeEach(async () => {
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [ChatLoadingIndicatorComponent],
    }).compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(ChatLoadingIndicatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------------------------------------------
  // Test di integrazione
  // ------------------------------------------------------
  describe('Test di integrazione', () => {
    it("Verifica che il componente venga creato", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che il template contenga l'elemento con classe 'loading-indicator'", () => {
      // Arrange:
      // Act:
      const container = fixture.nativeElement.querySelector('.loading-indicator');
      // Assert:
      expect(container).toBeTruthy();
    });

    it("Verifica che il template contenga un'immagine con src 'assets/banana.png'", () => {
      // Arrange:
      // Act:
      const img = fixture.nativeElement.querySelector('img');
      // Assert:
      expect(img).toBeTruthy();
      expect(img.src).toContain('assets/banana.png');
    });

    it("Verifica che l'immagine abbia alt 'Caricamento'", () => {
      // Arrange:
      // Act:
      const img = fixture.nativeElement.querySelector('img');
      // Assert:
      expect(img.alt).toBe('Caricamento');
    });
  });

  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------
  describe('Test di unità', () => {
    it("Verifica che l'istanza del componente sia definita", () => {
      // Arrange:
      const localComponent = new ChatLoadingIndicatorComponent();
      // Act:
      // Assert:
      expect(localComponent).toBeDefined();
    });
  });
});
