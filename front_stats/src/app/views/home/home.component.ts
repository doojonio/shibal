import { Component } from '@angular/core';
import { ChartConfiguration, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { CountPerHour, OperationsService } from '../../services/operations.service';
import { getLastHours } from '../../utils/dates';

@Component({
  selector: 'app-home',
  imports: [BaseChartDirective],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

  constructor(
    private operationsService: OperationsService,
  ) { }

  ngOnInit() {
    this.operationsService.getCountPerHour().subscribe(this.processOpCounts.bind(this))
  }

  public lineChartData: ChartConfiguration<'line'>['data'] | undefined

  public lineChartOptions: ChartOptions<'line'> = {
    responsive: false,
    scales: {
      y: {
        ticks: {
          stepSize: 1,
        }
      }
    }
  }
  public lineChartLegend = true;

  processOpCounts(counts: CountPerHour[]) {
    const last5Hours = getLastHours(5)

    const hourToCount = new Map()

    for (let [h, c] of counts) {
      hourToCount.set(h.getHours(), c)
    }

    const data = []
    for (const h of last5Hours) {
      const count = hourToCount.get(h.getHours())

      if (count === undefined) {
        data.push(0)
      }
      else {
        data.push(count)
      }
    }

    // this.lineChartData.labels = last5Hours.map(toString)
    this.lineChartData = {
      labels: last5Hours.map(h => h.getHours()),
      datasets: [
        {
          data: data,
          label: 'Operations per hour',
          fill: true,
          tension: 0.5,
          borderColor: 'black',
        }
      ]
    }
  }

}
