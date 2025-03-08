import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

export enum OrderTypes {
  START = 0,
  PAY = 1,
  PROMO = 2,
}

export interface Order {
  id: string
  user_id: string
  order_type: OrderTypes
  op_added: number
  created: Date
  payed: Date | null
}

@Injectable({
  providedIn: 'root'
})
export class OrdersService {
  baseUrl = "/api/v1/orders"

  constructor(private http: HttpClient) {
  }

  getOrders() {
    return this.http.get<Array<Order>>(this.baseUrl + "/list")
  }
}
