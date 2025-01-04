import { Component } from '@angular/core';
import { ChatComponent } from './chat/chat.component'; // Import the standalone component

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [ChatComponent], // Import the standalone component here
  standalone: true, // Mark AppComponent as standalone
})
export class AppComponent {}
