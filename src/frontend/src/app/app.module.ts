import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { ChatContainerComponent } from './chat/chat-container/chat-container.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    ChatContainerComponent,
    AppComponent,
  ],
  providers: [
    provideHttpClient(),
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
