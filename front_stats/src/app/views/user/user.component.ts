import { Component } from '@angular/core';

import { MatCardModule } from '@angular/material/card';
import { ActivatedRoute } from '@angular/router';
import { ChartOperationsTypesComponent } from '../../charts/operations-types/operations-types.component';
import { ChartOperationsComponent } from '../../charts/operations/operations.component';
import { ChartOrdersComponent } from '../../charts/orders/orders.component';
import { ChartTotalCuttedComponent } from '../../charts/total-cutted/total-cutted.component';
import { Order, OrdersService } from '../../services/orders.service';
import { TableOperationsComponent } from '../../tables/operations/operations.component';
import { TableOrdersComponent } from '../../tables/orders/orders.component';
import { User, UsersService } from '../../services/users.service';
import { DatePipe } from '@angular/common';


@Component({
  selector: 'app-user',
  imports: [
    MatCardModule,
    DatePipe,
    ChartOperationsComponent,
    ChartOrdersComponent,
    ChartOperationsTypesComponent,
    ChartTotalCuttedComponent,
    TableOperationsComponent,
    TableOrdersComponent,
  ],
  templateUrl: './user.component.html',
  styleUrl: './user.component.scss'
})
export class UserComponent {
  userId: string | undefined
  user: User | undefined

  constructor(
    private ordersService: OrdersService,
    private userSevice: UsersService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    let userId = this.route.snapshot.paramMap.get("id")
    if (userId) {
      this.userId = userId
    }

    this.ordersService.getOrders(this.userId).subscribe(orders => { this.orders = orders })
    if (this.userId) {
      this.userSevice.getUser(this.userId).subscribe(user => { this.user = user })
    }
  }

  displayedOrdersColumns = ['id', 'order_type', 'op_added', 'created', 'payed']

  orders: Order[] = []
}
