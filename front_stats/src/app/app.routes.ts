import { Routes } from '@angular/router';
import { UsersComponent } from './views/users/users.component';
import { UserComponent } from './views/user/user.component';
import { HomeComponent } from './views/home/home.component';

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
    },
    {
        path: 'users',
        component: UsersComponent
    },
    {
        path: 'user/:id',
        component: UserComponent,
    },
];
