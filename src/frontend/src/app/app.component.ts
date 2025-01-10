import { Component } from '@angular/core';
import { ChatContainerComponent } from './chat/chat-container/chat-container.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [ChatContainerComponent],
})
export class AppComponent {}
