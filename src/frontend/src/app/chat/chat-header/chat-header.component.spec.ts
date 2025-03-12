import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatHeaderComponent } from './chat-header.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { By } from '@angular/platform-browser';

describe('ChatHeaderComponent', () => {
  let component: ChatHeaderComponent;
  let fixture: ComponentFixture<ChatHeaderComponent>;

  beforeEach(async () => {
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [ChatHeaderComponent, HttpClientTestingModule],
    }).compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(ChatHeaderComponent);
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

    it("Verifica che il titolo contenga 'BuddyBot'", () => {
      // Arrange:
      // Act:
      const h1 = fixture.nativeElement.querySelector('h1');
      // Assert:
      expect(h1.textContent).toContain('BuddyBot');
    });

    it("Verifica che l'elemento app-chat-badge sia presente", () => {
      // Arrange:
      // Act:
      const badgeElement = fixture.debugElement.query(By.css('app-chat-badge'));
      // Assert:
      expect(badgeElement).toBeTruthy();
    });

    it("Verifica che l'immagine del logo abbia src e alt corretti", () => {
      // Arrange:
      // Act:
      const img = fixture.nativeElement.querySelector('.logo-container img');
      // Assert:
      expect(img.src).toContain('assets/sweg_logo_sito.png');
      expect(img.alt).toBe('Logo');
    });

    it("Verifica che il tag header abbia la classe 'chat-header'", () => {
      // Arrange:
      // Act:
      const headerEl = fixture.nativeElement.querySelector('header');
      // Assert:
      expect(headerEl.classList).toContain('chat-header');
    });
  });

  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------
  describe('Test di unità', () => {
    it("Verifica che l'istanza del componente sia definita", () => {
      // Arrange:
      const localComponent = new ChatHeaderComponent();
      // Act:
      // Assert:
      expect(localComponent).toBeDefined();
    });
  });
});
