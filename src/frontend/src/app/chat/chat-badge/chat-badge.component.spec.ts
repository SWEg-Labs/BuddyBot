import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatBadgeComponent } from './chat-badge.component';
import { ChatService } from '../chat.service';
import { DatabaseService } from '../database.service';
import { LastLoadOutcome } from '../../models/badge.model';
import { Subject } from 'rxjs';

describe('ChatBadgeComponent', () => {
  let component: ChatBadgeComponent;
  let fixture: ComponentFixture<ChatBadgeComponent>;
  let mockDatabaseService: any;
  let mockDatabaseServiceSpy: any;
  let lastLoadOutcomeSubject: Subject<LastLoadOutcome>;

  beforeEach(async () => {
    // Arrange:
    mockDatabaseServiceSpy = { checkFileUpdates: jasmine.createSpy('checkFileUpdates') };
    lastLoadOutcomeSubject = new Subject<LastLoadOutcome>();
    mockDatabaseService = { lastLoadOutcome$: lastLoadOutcomeSubject.asObservable() };
    // Arrange:
    await TestBed.configureTestingModule({
      imports: [ChatBadgeComponent],
      providers: [
        { provide: DatabaseService, useValue: mockDatabaseServiceSpy },
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

    it("Verifica che, durante l'inizializzazione di ChatBadgeComponent, la sottoscrizione a lastLoadOutcome$ di DatabaseService " +
      "aggiorni l'attributo lastLoadOutcome di ChatBadgeComponent", () => {
      // Arrange:
      component.ngOnInit();
      // Act:
      lastLoadOutcomeSubject.next(LastLoadOutcome.ERROR);
      // Assert:
      expect(component.lastLoadOutcome).toBe(LastLoadOutcome.ERROR);
    });

    it("Verifica che, al cambio di valore di lastLoadOutcome$ in DatabaseService, l'attributo lastLoadOutcome " +
      "di ChatBadgeComponent venga aggiornato", () => {
      // Arrange:
      const nuovoValore = LastLoadOutcome.FALSE;
      // Act:
      lastLoadOutcomeSubject.next(nuovoValore);
      fixture.detectChanges();
      // Assert:
      expect(component.lastLoadOutcome).toBe(nuovoValore);
    });
  });

  // ------------------------------------------------------
  // Test di unità
  // ------------------------------------------------------
  describe('Test di unità', () => {
    let localComponent: ChatBadgeComponent;
    let localDatabaseService: any;
    let localSubject: Subject<LastLoadOutcome>;

    beforeEach(() => {
      // Arrange:
      localSubject = new Subject<LastLoadOutcome>();
      localDatabaseService = { lastLoadOutcome$: localSubject.asObservable() };
      // Arrange:
      localComponent = new ChatBadgeComponent(localDatabaseService);
    });

    it("Verifica che il valore iniziale dell'attributo lastLoadOutcome di ChatBadgeComponent sia TRUE", () => {
      // Arrange:
      // Act:
      // Assert:
      expect(localComponent.lastLoadOutcome).toBe(LastLoadOutcome.TRUE);
    });

    it("Verifica che il getter isUpdated di ChatBadgeComponent restituisca il valore corretto, corrispondente all'attributo " +
      "lastLoadOutcome", () => {
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
  });
});
