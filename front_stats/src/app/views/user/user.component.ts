import { DatePipe, DecimalPipe, JsonPipe } from '@angular/common';
import { Component } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { ActivatedRoute } from '@angular/router';
import { ChartOperationsTypesComponent } from '../../charts/operations-types/operations-types.component';
import { ChartOperationsComponent } from '../../charts/operations/operations.component';
import { ChartOrdersComponent } from '../../charts/orders/orders.component';
import { OpTypePipe } from '../../pipes/op-type.pipe';
import { OrderTypePipe } from '../../pipes/order-type.pipe';
import { Order, OrdersService } from '../../services/orders.service';
import { TableOperationsComponent } from '../../tables/operations/operations.component';
import { TableOrdersComponent } from '../../tables/orders/orders.component';


@Component({
  selector: 'app-user',
  imports: [
    ChartOperationsComponent,
    ChartOrdersComponent,
    ChartOperationsTypesComponent,
    TableOperationsComponent,
    TableOrdersComponent,
  ],
  templateUrl: './user.component.html',
  styleUrl: './user.component.scss'
})
export class UserComponent {
  userId: string | undefined

  constructor(
    private ordersService: OrdersService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    let userId = this.route.snapshot.paramMap.get("id")
    if (userId) {
      this.userId = userId
    }

    this.ordersService.getOrders(this.userId).subscribe(orders => { this.orders = orders })
  }

  displayedOrdersColumns = ['id', 'order_type', 'op_added', 'created', 'payed']

  orders: Order[] = []
}
