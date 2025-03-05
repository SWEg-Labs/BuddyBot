import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatSuggestionsComponent } from './chat-suggestions.component';
import { ChatService } from '../chat.service';
import { of } from 'rxjs';

describe('ChatSuggestionsComponent', () => {
  let component: ChatSuggestionsComponent;
  let fixture: ComponentFixture<ChatSuggestionsComponent>;
  let chatServiceSpy: jasmine.SpyObj<ChatService>;

  beforeEach(async () => {
    // Arrange
    chatServiceSpy = jasmine.createSpyObj('ChatService', [
      'getContinuationSuggestions'
    ]);
    chatServiceSpy.getContinuationSuggestions.and.returnValue(of(['Cont1', 'Cont2']));

    await TestBed.configureTestingModule({
      imports: [ ChatSuggestionsComponent ],
      providers: [
        { provide: ChatService, useValue: chatServiceSpy }
      ]
    }).compileComponents();
  });

  beforeEach(() => {
    // Act
    fixture = TestBed.createComponent(ChatSuggestionsComponent);
    component = fixture.componentInstance;
  });

  // ------------------- Unit -------------------
  it('should create the ChatSuggestionsComponent instance successfully', () => {
    // Arrange
    fixture.detectChanges();

    // Assert
    expect(component).toBeTruthy();
  });

  // -------------- Integration -----------------
  it('should call chatService.getContinuationSuggestions() if lastMessageTimestamp is within 5 minutes', () => {
    // Arrange
    component.lastMessageTimestamp = Date.now();

    // Act
    fixture.detectChanges(); // ngOnInit

    // Assert
    expect(component.showInitial).toBeFalse();
    expect(component.continuationSuggestions).toEqual(['Cont1', 'Cont2']);
    expect(chatServiceSpy.getContinuationSuggestions).toHaveBeenCalled();
  });

  // ------------------- Unit -------------------
  it('should emit suggestionClicked when onSuggestionClick() is invoked', () => {
    // Arrange
    spyOn(component.suggestionClicked, 'emit');
    const suggestion = 'Prova';

    // Act
    component.onSuggestionClick(suggestion);

    // Assert
    expect(component.suggestionClicked.emit).toHaveBeenCalledWith('Prova');
  });
});
