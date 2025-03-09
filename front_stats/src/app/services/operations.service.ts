import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map } from 'rxjs';

export enum OperationTypes {
  TRIM = 0,
  CUT = 1,
  VOLUME = 2,
  FADES = 3,
}

export interface Operation {
  id: string
  user_id: string
  op_type: OperationTypes
  details: object
  started: Date
  took: number | null
}

export type CountPerHour = [Date, number];

@Injectable({
  providedIn: 'root'
})
export class OperationsService {
  baseUrl = "/api/v1/operations"

  constructor(private http: HttpClient) {
  }

  getCountPerHour(userId: string | undefined = undefined) {

    let params = new HttpParams()

    if (userId != undefined) {
      params = params.set("user_id", userId)
    }

    return this.http.get<[string, number][]>(this.baseUrl + "/count_per_hour", { params }).pipe(
      // FIXME: return utc date on backend
      map(counts => counts.map(c => [new Date(c[0] + "Z"), c[1]] as CountPerHour))
    )
  }

  getCountPerType(userId: string | undefined = undefined) {

    let params = new HttpParams()

    if (userId != undefined) {
      params = params.set("user_id", userId)
    }

    return this.http.get<[OperationTypes, number][]>(this.baseUrl + "/count_per_type", { params })
  }

  getOperations(userId: string | undefined = undefined) {
    let params = new HttpParams()

    if (userId != undefined) {
      params = params.set("user_id", userId)
    }

    return this.http.get<Array<Operation>>(this.baseUrl + "/list", { params })
  }

  getCuttedPerDay(userId: string | undefined = undefined, days: number = 5) {
    let params = (new HttpParams()).set("days", days)

    if (userId != undefined) {
      params = params.set("user_id", userId)
    }

    return this.http.get<[string, number][]>(this.baseUrl + "/total_cutted_per_day", { params })
  }
}
