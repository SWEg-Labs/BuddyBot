import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import { ChatContainerComponent } from './chat-container/chat-container.component';
import { ChatHeaderComponent } from './chat-header/chat-header.component';
import { ChatBadgeComponent } from './chat-badge/chat-badge.component';
import { ChatMessagesComponent } from './chat-messages/chat-messages.component';
import { ChatSuggestionsComponent } from './chat-suggestions/chat-suggestions.component';
import { ChatInputComponent } from './chat-input/chat-input.component';
import { ChatLoadingIndicatorComponent } from './chat-loading-indicator/chat-loading-indicator.component';

@NgModule({
  declarations: [
    ChatContainerComponent,
    ChatHeaderComponent,
    ChatBadgeComponent,
    ChatMessagesComponent,
    ChatSuggestionsComponent,
    ChatInputComponent,
    ChatLoadingIndicatorComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
  ],
  exports: [
    ChatContainerComponent
  ],
  providers: [
  ]
})
export class ChatModule {}
