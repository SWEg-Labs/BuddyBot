import { Component } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { AppComponent } from './app.component';

@Component({
  selector: 'app-chat-container',
  template: '<div class="stub-chat-container">Stub Chat Container</div>',
  standalone: true,
})
class StubChatContainerComponent {}

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async () => {
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [AppComponent, HttpClientTestingModule],
    })
      .overrideComponent(AppComponent, {
        set: { imports: [StubChatContainerComponent, HttpClientTestingModule] },
      })
      .compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------------------------------------------
  // Test di integrazione
  // ------------------------------------------------------
  describe('Test di integrazione', () => {
    it("Verifica che il componente venga creato", () => {
      // Act & Assert:
      expect(component).toBeTruthy();
    });

    it("Verifica che il template contenga l'elemento app-chat-container", () => {
      // Act:
      const containerElem = fixture.nativeElement.querySelector('app-chat-container');
      // Assert:
      expect(containerElem).toBeTruthy();
    });

    it("Verifica che il contenuto del chat container venga renderizzato", () => {
      // Act:
      const stubElement = fixture.nativeElement.querySelector('.stub-chat-container');
      // Assert:
      expect(stubElement).toBeTruthy();
      expect(stubElement.textContent).toContain("Stub Chat Container");
    });
  });

  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------
  describe('Test di unità', () => {
    it("Verifica che l'istanza del componente sia definita", () => {
      // Act:
      const localComponent = new AppComponent();
      // Assert:
      expect(localComponent).toBeDefined();
    });
  });
});
