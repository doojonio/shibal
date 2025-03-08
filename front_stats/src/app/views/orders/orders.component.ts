import { Component } from '@angular/core';
import { TableOrdersComponent } from '../../tables/orders/orders.component';

@Component({
  selector: 'app-orders',
  imports: [TableOrdersComponent],
  templateUrl: './orders.component.html',
  styleUrl: './orders.component.scss'
})
export class OrdersComponent {
}
