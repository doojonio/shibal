import { Component, Input } from '@angular/core';
import { ChartConfiguration } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { OperationsService } from '../../services/operations.service';
import { getLastDays } from '../../utils/dates';

@Component({
  selector: 'app-charts-total-cutted',
  imports: [BaseChartDirective],
  templateUrl: './total-cutted.component.html',
  styleUrl: './total-cutted.component.scss'
})
export class ChartTotalCuttedComponent {
  @Input() userId: string | undefined = undefined

  public barChartLegend = true;
  public barChartPlugins = [];

  public barChartData: ChartConfiguration<'bar'>['data'] | undefined;

  public barChartOptions: ChartConfiguration<'bar'>['options'] = {
    responsive: false,
  };

  constructor(private opService: OperationsService) { }

  ngOnInit() {
    this.opService.getCuttedPerDay(this.userId, 5).subscribe(this.processData.bind(this))
  }

  processData(counts: [string, number][]) {
    const daysToCount = new Map<number, number>()
    for (const rec of counts) {
      const key = (new Date(rec[0])).getDate();
      daysToCount.set(key, rec[1])
    }

    const labels = []
    const data = []
    const last5Days = getLastDays(5)
    for (const day of last5Days) {
      labels.push(day.getDate())
      data.push(daysToCount.get(day.getDate()) || 0)
    }

    this.barChartData = {
      labels: labels,
      datasets: [
        { data, label: 'Cutted ms' },
      ]
    }
  }


}
