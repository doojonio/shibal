import { Component } from '@angular/core';
import { ChartOperationsTypesComponent } from '../../charts/operations-types/operations-types.component';
import { ChartOperationsComponent } from '../../charts/operations/operations.component';
import { TableOperationsComponent } from '../../tables/operations/operations.component';

@Component({
  selector: 'app-operations',
  imports: [TableOperationsComponent, ChartOperationsComponent, ChartOperationsTypesComponent],
  templateUrl: './operations.component.html',
  styleUrl: './operations.component.scss'
})
export class OperationsComponent {

}
