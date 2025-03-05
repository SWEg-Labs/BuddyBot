import { SafeHtml } from "@angular/platform-browser";

export interface Message {
    sender: string;
    text: SafeHtml;
    copied?: boolean;
  }
  