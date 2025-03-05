import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatLoadingIndicatorComponent } from './chat-loading-indicator.component';

describe('ChatLoadingIndicatorComponent', () => {
  let component: ChatLoadingIndicatorComponent;
  let fixture: ComponentFixture<ChatLoadingIndicatorComponent>;

  beforeEach(async () => {
    // Arrange
    await TestBed.configureTestingModule({
      imports: [ ChatLoadingIndicatorComponent ]
    }).compileComponents();
  });

  beforeEach(() => {
    // Act
    fixture = TestBed.createComponent(ChatLoadingIndicatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------- Unit -------------------
  it('should create the ChatLoadingIndicatorComponent instance successfully', () => {
    // Assert
    expect(component).toBeTruthy();
  });

  // ------------------- Unit -------------------
  it('should contain an image with the rotating-logo class', () => {
    // Arrange
    const compiled = fixture.nativeElement as HTMLElement;

    // Act
    const img = compiled.querySelector('img.rotating-logo');

    // Assert
    expect(img).toBeTruthy();
  });
});
