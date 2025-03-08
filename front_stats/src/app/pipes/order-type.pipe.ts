import { Pipe, PipeTransform } from '@angular/core';
import { OrderTypes } from '../services/orders.service';

@Pipe({
  name: 'orderType'
})
export class OrderTypePipe implements PipeTransform {

  transform(value: OrderTypes): string {
    return OrderTypes[value];
  }

}
