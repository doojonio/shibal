import { DatePipe, DecimalPipe, JsonPipe } from '@angular/common';
import { Component } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { OpTypePipe } from '../../pipes/op-type.pipe';
import { OrderTypePipe } from '../../pipes/order-type.pipe';
import { Operation, OperationsService } from '../../services/operations.service';
import { Order, OrdersService } from '../../services/orders.service';


@Component({
  selector: 'app-user',
  imports: [MatTableModule, DatePipe, DecimalPipe, JsonPipe, OpTypePipe, OrderTypePipe],
  templateUrl: './user.component.html',
  styleUrl: './user.component.scss'
})
export class UserComponent {

  constructor(
    private ordersService: OrdersService,
    private operationsService: OperationsService,
  ) { }

  ngOnInit() {
    this.operationsService.getOperations().subscribe(ops => { this.operations = ops; console.log(ops) })
    this.ordersService.getOrders().subscribe(orders => { this.orders = orders })
  }

  displayedOpColumns = ['id', 'op_type', 'started', 'took', 'details']
  displayedOrdersColumns = ['id', 'order_type', 'op_added', 'created', 'payed']

  operations: Operation[] = []
  orders: Order[] = []
}
