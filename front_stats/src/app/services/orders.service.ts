import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Dictionary } from '../utils/types';
import { map } from 'rxjs';

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

  getOrders(userId: string | undefined = undefined) {
    let params = new HttpParams()

    if (userId != undefined) {
      params = params.set("user_id", userId)
    }

    return this.http.get<Array<Order>>(this.baseUrl + "/list", { params })
  }

  getCountPerDay(maxDays: number, userId: string | undefined = undefined) {
    let params = (new HttpParams()).set("days", maxDays)
    if (userId != undefined) {
      params = params.set("user_id", userId)
    }

    return this.http.get<any>(this.baseUrl + "/count_per_day", { params }).pipe(
      map(dict => {
        const dictDate = new Map<number, number>();
        for (let k in dict) {
          dictDate.set((new Date(k)).getDate(), dict[k])
        }

        return dictDate
      })
    )
  }
}
