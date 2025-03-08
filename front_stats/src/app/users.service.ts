import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

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
}
