import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatBadgeComponent } from './chat-badge.component';
import { ChatService } from '../chat.service';
import { DatabaseService } from '../database.service';
import { LastLoadOutcome } from '../../models/badge.model';
import { Subject } from 'rxjs';

describe('ChatBadgeComponent', () => {
  let component: ChatBadgeComponent;
  let fixture: ComponentFixture<ChatBadgeComponent>;
  let mockChatService: any;
  let mockDatabaseService: any;
  let lastLoadOutcomeSubject: Subject<LastLoadOutcome>;

  beforeEach(async () => {
    // Arrange:
    mockChatService = { checkFileUpdates: jasmine.createSpy('checkFileUpdates') };
    lastLoadOutcomeSubject = new Subject<LastLoadOutcome>();
    mockDatabaseService = { lastLoadOutcome$: lastLoadOutcomeSubject.asObservable() };
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [ChatBadgeComponent],
      providers: [
        { provide: ChatService, useValue: mockChatService },
        { provide: DatabaseService, useValue: mockDatabaseService },
      ],
    }).compileComponents();
    // Arrange:
    fixture = TestBed.createComponent(ChatBadgeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // ------------------------------------------------------
  // Test di integrazione
  // ------------------------------------------------------
  describe('Test di integrazione', () => {
    it("Verifica che il valore iniziale di lastLoadOutcome sia TRUE", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(component.lastLoadOutcome).toBe(LastLoadOutcome.TRUE);
    });

    it("Verifica che, al cambio di valore di lastLoadOutcome$, la proprietà lastLoadOutcome venga aggiornata", () => {
      // Arrange:
      const nuovoValore = LastLoadOutcome.FALSE;
      // Act:
      lastLoadOutcomeSubject.next(nuovoValore);
      fixture.detectChanges();
      // Assert:
      expect(component.lastLoadOutcome).toBe(nuovoValore);
    });

    it("Verifica che il getter isUpdated restituisca true se lastLoadOutcome è TRUE", () => {
      // Arrange:
      component.lastLoadOutcome = LastLoadOutcome.TRUE;
      // Act:
      const isUpdated = component.isUpdated;
      // Assert:
      expect(isUpdated).toBeTrue();
    });

    it("Verifica che il getter isUpdated restituisca false se lastLoadOutcome non è TRUE", () => {
      // Arrange:
      component.lastLoadOutcome = LastLoadOutcome.ERROR;
      // Act:
      const isUpdated = component.isUpdated;
      // Assert:
      expect(isUpdated).toBeFalse();
    });

    it("Verifica che, alla chiamata del metodo onToggleStatus, venga chiamato il metodo checkFileUpdates di ChatService", () => {
      // Arrange:
      // Act:
      component.onToggleStatus();
      // Assert:
      expect(mockChatService.checkFileUpdates).toHaveBeenCalled();
    });
  });

  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------
  describe('Test di unità', () => {
    let localComponent: ChatBadgeComponent;
    let localChatService: any;
    let localDatabaseService: any;
    let localSubject: Subject<LastLoadOutcome>;

    beforeEach(() => {
      // Arrange:
      localChatService = { checkFileUpdates: jasmine.createSpy('checkFileUpdates') };
      localSubject = new Subject<LastLoadOutcome>();
      localDatabaseService = { lastLoadOutcome$: localSubject.asObservable() };
      // Arrange:
      localComponent = new ChatBadgeComponent(localChatService, localDatabaseService);
    });

    it("Verifica che il valore iniziale di lastLoadOutcome sia TRUE", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(localComponent.lastLoadOutcome).toBe(LastLoadOutcome.TRUE);
    });

    it("Verifica che, durante l'inizializzazione, la sottoscrizione a lastLoadOutcome$ aggiorni lastLoadOutcome", () => {
      // Arrange:
      localComponent.ngOnInit();
      // Act:
      localSubject.next(LastLoadOutcome.ERROR);
      // Assert:
      expect(localComponent.lastLoadOutcome).toBe(LastLoadOutcome.ERROR);
    });

    it("Verifica che il getter isUpdated restituisca il valore corretto in base a lastLoadOutcome", () => {
      // Arrange:
      localComponent.lastLoadOutcome = LastLoadOutcome.TRUE;
      // Act:
      let result = localComponent.isUpdated;
      // Assert:
      expect(result).toBeTrue();
      // Arrange:
      localComponent.lastLoadOutcome = LastLoadOutcome.FALSE;
      // Act:
      result = localComponent.isUpdated;
      // Assert:
      expect(result).toBeFalse();
    });

    it("Verifica che, alla chiamata del metodo onToggleStatus, venga invocato il metodo checkFileUpdates di ChatService", () => {
      // Arrange:
      // Act:
      localComponent.onToggleStatus();
      // Assert:
      expect(localChatService.checkFileUpdates).toHaveBeenCalled();
    });
  });
});
