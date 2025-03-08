import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterLink, RouterOutlet } from '@angular/router';
import { UsersComponent } from './views/users/users.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,

    MatIconModule,
    MatButtonModule,
    MatToolbarModule,

    RouterLink,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  constructor() { }
}
