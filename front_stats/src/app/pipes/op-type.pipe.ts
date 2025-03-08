import { Pipe, PipeTransform } from '@angular/core';
import { OperationTypes } from '../services/operations.service';

@Pipe({
  name: 'opType'
})
export class OpTypePipe implements PipeTransform {

  transform(value: OperationTypes): string {
    return OperationTypes[value]
  }
}
