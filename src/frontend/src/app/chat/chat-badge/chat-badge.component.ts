import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LastLoadOutcome } from '../../models/badge.model';
import { DatabaseService } from '../database.service';

@Component({
  standalone: true,
  selector: 'app-chat-badge',
  templateUrl: './chat-badge.component.html',
  styleUrls: ['./chat-badge.component.scss'],
  imports: [CommonModule],
})
export class ChatBadgeComponent implements OnInit {
  lastLoadOutcome: LastLoadOutcome = LastLoadOutcome.TRUE
  public LastLoadOutcome = LastLoadOutcome

  constructor(private readonly databaseService: DatabaseService) {}

  ngOnInit(): void {
    this.databaseService.lastLoadOutcome$.subscribe({
      next: (outcome: LastLoadOutcome) => {
        this.lastLoadOutcome = outcome
      }
    })
  }

  get isUpdated(): boolean {
    return this.lastLoadOutcome === LastLoadOutcome.TRUE
  }
}
