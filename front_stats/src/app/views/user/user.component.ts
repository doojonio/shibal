import { DatePipe, DecimalPipe, JsonPipe } from '@angular/common';
import { Component } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { OpTypePipe } from '../../pipes/op-type.pipe';
import { OrderTypePipe } from '../../pipes/order-type.pipe';
import { Operation, OperationsService } from '../../services/operations.service';
import { Order, OrdersService } from '../../services/orders.service';
import { ChartOperationsComponent } from '../../charts/operations/operations.component';
import { ChartOrdersComponent } from '../../charts/orders/orders.component';
import { ActivatedRoute } from '@angular/router';
import { ChartOperationsTypesComponent } from '../../charts/operations-types/operations-types.component';


@Component({
  selector: 'app-user',
  imports: [
    MatTableModule,
    DatePipe,
    DecimalPipe,
    JsonPipe,
    OpTypePipe,
    OrderTypePipe,
    ChartOperationsComponent,
    ChartOrdersComponent,
    ChartOperationsTypesComponent,
  ],
  templateUrl: './user.component.html',
  styleUrl: './user.component.scss'
})
export class UserComponent {
  userId: string | undefined

  constructor(
    private ordersService: OrdersService,
    private operationsService: OperationsService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    let userId = this.route.snapshot.paramMap.get("id")
    if (userId) {
      this.userId = userId
    }

    this.operationsService.getOperations(this.userId).subscribe(ops => { this.operations = ops })
    this.ordersService.getOrders(this.userId).subscribe(orders => { this.orders = orders })
  }

  displayedOpColumns = ['id', 'op_type', 'started', 'took', 'details']
  displayedOrdersColumns = ['id', 'order_type', 'op_added', 'created', 'payed']

  operations: Operation[] = []
  orders: Order[] = []
}
