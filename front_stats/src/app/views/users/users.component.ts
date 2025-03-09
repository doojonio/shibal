import { DatePipe } from '@angular/common';
import { Component } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { RouterLink } from '@angular/router';
import { User, UsersService } from '../../services/users.service';

@Component({
  selector: 'app-users',
  imports: [
    MatTableModule,
    DatePipe,
    RouterLink,
  ],
  templateUrl: './users.component.html',
  styleUrl: './users.component.scss'
})
export class UsersComponent {
  displayedColumns: string[] = ['id', 'chat_id', 'op_balance', 'created'];

  constructor(
    private usersService: UsersService,
  ) { }

  ngOnInit() {
    this.usersService.getUsers().subscribe(users => { this.users = users });
  }


  public users: Array<User> = []
}
