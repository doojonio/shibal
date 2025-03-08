import { DatePipe, DecimalPipe, JsonPipe } from '@angular/common';
import { Component, Input } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { OrderTypePipe } from '../../pipes/order-type.pipe';
import { Order, OrdersService } from '../../services/orders.service';

@Component({
  selector: 'app-tables-orders',
  imports: [
    MatTableModule,
    DatePipe,
    OrderTypePipe,
  ],
  templateUrl: './orders.component.html',
  styleUrl: './orders.component.scss'
})
export class TableOrdersComponent {
  @Input() userId: string | undefined

  orders: Order[] = []
  displayedColumns = ['id', 'order_type', 'op_added', 'created', 'payed']

  constructor(
    private ordersService: OrdersService,
  ) { }

  ngOnInit() {
    this.ordersService.getOrders(this.userId).subscribe(orders => { this.orders = orders })
  }
}
