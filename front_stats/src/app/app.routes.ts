import { Routes } from '@angular/router';
import { UsersComponent } from './views/users/users.component';
import { UserComponent } from './views/user/user.component';
import { HomeComponent } from './views/home/home.component';
import { OrdersComponent } from './views/orders/orders.component';
import { OperationsComponent } from './views/operations/operations.component';

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent,
    },
    {
        path: 'users',
        component: UsersComponent,
    },
    {
        path: 'orders',
        component: OrdersComponent,
    },
    {
        path: 'operations',
        component: OperationsComponent,
    },
    {
        path: 'user/:id',
        component: UserComponent,
    },
];
