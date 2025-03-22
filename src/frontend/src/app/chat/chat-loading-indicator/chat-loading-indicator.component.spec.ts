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
  // Test di unità
  // ------------------------------------------------------

  describe('Test di unità', () => {
    it("Verifica che il componente ChatLoadingIndicatorComponent venga creato", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che l'istanza del componente ChatLoadingIndicatorComponent sia definita", () => {
      // Arrange:
      const localComponent = new ChatLoadingIndicatorComponent();
      // Act:
      // Assert:
      expect(localComponent).toBeDefined();
    });

    it("Verifica che il template HTML di ChatLoadingIndicatorComponent contenga l'elemento con classe CSS 'loading-indicator'", () => {
      // Arrange:
      // Act:
      const container = fixture.nativeElement.querySelector('.loading-indicator');
      // Assert:
      expect(container).toBeTruthy();
    });

    it("Verifica che il template HTML di ChatLoadingIndicatorComponent contenga un'immagine con attributo src 'assets/banana.png'", () => {
      // Arrange:
      // Act:
      const img = fixture.nativeElement.querySelector('img');
      // Assert:
      expect(img).toBeTruthy();
      expect(img.src).toContain('assets/banana.png');
    });

    it("Verifica che il template HTML di ChatLoadingIndicatorComponent contenga un'immagine con attributo alt 'Caricamento'", () => {
      // Arrange:
      // Act:
      const img = fixture.nativeElement.querySelector('img');
      // Assert:
      expect(img.alt).toBe('Caricamento');
    });
  });
});
