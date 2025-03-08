import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map } from 'rxjs';

export interface IUser {
  id: string
  chat_id: number
  op_balance: number
  created: Date
}

@Injectable({
  providedIn: 'root'
})
export class UsersService {
  baseUrl = "/api/v1/users"

  constructor(private http: HttpClient) {
  }

  getUsers() {
    return this.http.get<Array<IUser>>(this.baseUrl + "/list")
  }

  getCountPerDay(maxDays: number) {
    return this.http.get<any>(this.baseUrl + "/count_per_day", { params: { days: maxDays } }).pipe(
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
