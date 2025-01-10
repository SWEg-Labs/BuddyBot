import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  standalone: true,
  selector: 'app-chat-actions',
  templateUrl: './chat-actions.component.html',
  styleUrls: ['./chat-actions.component.scss'],
  imports: [CommonModule],
})
export class ChatActionsComponent {
  @Input() isLoading = false;

  @Output() jira = new EventEmitter<void>();
  @Output() github = new EventEmitter<void>();
  @Output() confluence = new EventEmitter<void>();

  onJiraClick() {
    this.jira.emit();
  }

  onGithubClick() {
    this.github.emit();
  }

  onConfluenceClick() {
    this.confluence.emit();
  }
}
