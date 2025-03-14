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
  // Test di unità
  // ------------------------------------------------------

  describe('Test di unità', () => {
    it("Verifica che il componente ChatHeaderComponent venga creato", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che l'istanza del componente ChatHeaderComponent sia definita", () => {
      // Arrange:
      const localComponent = new ChatHeaderComponent();
      // Act:
      // Assert:
      expect(localComponent).toBeDefined();
    });

    it("Verifica che il titolo h1 del template HTML di ChatHeaderComponent contenga 'BuddyBot'", () => {
      // Arrange:
      // Act:
      const h1 = fixture.nativeElement.querySelector('h1');
      // Assert:
      expect(h1.textContent).toContain('BuddyBot');
    });

    it("Verifica che il tag app-chat-badge sia presente nel template HTML di ChatHeaderComponent", () => {
      // Arrange:
      // Act:
      const badgeElement = fixture.debugElement.query(By.css('app-chat-badge'));
      // Assert:
      expect(badgeElement).toBeTruthy();
    });

    it("Verifica che l'immagine del logo di ChatHeaderComponent, in HTML, abbia gli attributi src e alt corretti", () => {
      // Arrange:
      // Act:
      const img = fixture.nativeElement.querySelector('.logo-container img');
      // Assert:
      expect(img.src).toContain('assets/sweg_logo_sito.png');
      expect(img.alt).toBe('Logo');
    });

    it("Verifica che il tag header del template HTML di ChatHeaderComponent abbia la classe CSS 'chat-header'", () => {
      // Arrange:
      // Act:
      const headerEl = fixture.nativeElement.querySelector('header');
      // Assert:
      expect(headerEl.classList).toContain('chat-header');
    });
  });
});
