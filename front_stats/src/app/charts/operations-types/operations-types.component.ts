import { Component, Input } from '@angular/core';
import { ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { OperationsService, OperationTypes } from '../../services/operations.service';

@Component({
  selector: 'app-charts-operations-types',
  imports: [BaseChartDirective],
  templateUrl: './operations-types.component.html',
  styleUrl: './operations-types.component.scss'
})
export class ChartOperationsTypesComponent {
  @Input() userId: string | undefined = undefined

  // Pie
  public pieChartOptions: ChartOptions<'pie'> = {
    responsive: false,
  };
  public pieChartLabels: string[] | undefined;
  public pieChartDatasets: { data: number[] }[] | undefined;
  public pieChartLegend = true;
  public pieChartPlugins = [];

  constructor(
    private operationsService: OperationsService,
  ) { }

  ngOnInit() {
    this.operationsService.getCountPerType(this.userId).subscribe(this.processData.bind(this))
  }

  processData(counts: [OperationTypes, number][]) {
    const labels = []
    const data = []
    for (let [opType, count] of counts) {
      labels.push(OperationTypes[opType]);
      data.push(count)
    }

    this.pieChartLabels = labels
    this.pieChartDatasets = [{ data }]
  }
}
