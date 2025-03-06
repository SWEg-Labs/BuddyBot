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

  // Test di Unità
  it('deve creare correttamente l’istanza di ChatLoadingIndicatorComponent', () => {
    expect(component).toBeTruthy();
  });

  // Test di Unità
  it('deve contenere un’immagine con la classe rotating-logo', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const img = compiled.querySelector('img.rotating-logo');
    expect(img).toBeTruthy();
  });
});
