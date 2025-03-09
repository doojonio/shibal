import { Component, Input } from '@angular/core';
import { ChartConfiguration, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { OrdersService } from '../../services/orders.service';
import { getLastDays } from '../../utils/dates';

@Component({
  selector: 'app-charts-orders',
  imports: [BaseChartDirective],
  templateUrl: './orders.component.html',
  styleUrl: './orders.component.scss'
})
export class ChartOrdersComponent {
  @Input() userId: string | undefined = undefined

  constructor(
    private ordersService: OrdersService,
  ) { }

  ngOnInit() {
    this.ordersService.getCountPerDay(5, this.userId).subscribe(this.processOrderCounts.bind(this))
  }

  public lineChartLegend = true;
  public lineChartData: ChartConfiguration<'line'>['data'] | undefined
  public lineChartOptions: ChartOptions<'line'> = {
    responsive: false,
    scales: {
      y: {
        ticks: {
          stepSize: 1,
        },
        suggestedMin: 0,
        beginAtZero: true,
      }
    }
  }

  processOrderCounts(counts: Map<number, number>) {
    const last5Days = getLastDays(5)

    const data = []
    for (const h of last5Days) {
      const count = counts.get(h.getDate())

      if (count === undefined) {
        data.push(0)
      }
      else {
        data.push(count)
      }
    }

    this.lineChartData = {
      labels: last5Days.map(h => h.getDate()),
      datasets: [
        {
          data: data,
          label: 'Orders per day',
          fill: true,
          tension: 0.5,
          borderColor: 'black',
        }
      ]
    }
  }

}
