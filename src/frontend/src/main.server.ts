import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { config } from './app/app.config.server';

export default function bootstrap() {
  return bootstrapApplication(AppComponent, {
    ...config,
    providers: [
      provideHttpClient(withFetch()),
    ],
  });
}
