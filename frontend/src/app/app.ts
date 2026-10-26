import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterLinkWithHref, RouterLink } from '@angular/router';

@Component({
  imports: [RouterOutlet],
  selector: 'app-root',
  styleUrl: './app.scss',
  templateUrl: './app.html',
})
export class App {
  title = signal('mouad');
}
