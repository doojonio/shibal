import { HttpClient } from '@angular/common/http';
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

  getCountPerHour() {

    return this.http.get<[string, number][]>(this.baseUrl + "/count_per_hour").pipe(
      // FIXME: return utc date on backend
      map(counts => counts.map(c => [new Date(c[0] + "Z"), c[1]] as CountPerHour ))
    )
  }

  getOperations() {
    return this.http.get<Array<Operation>>(this.baseUrl + "/list")
  }
}
