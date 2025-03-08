import { Component } from '@angular/core';
import { ChartConfiguration, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { OrdersService } from '../../services/orders.service';
import { UsersService } from '../../services/users.service';
import { getLastDays } from '../../utils/dates';
import { ChartOperationsComponent } from '../../charts/operations/operations.component';

@Component({
  selector: 'app-home',
  imports: [BaseChartDirective, ChartOperationsComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

  constructor(
    private ordersService: OrdersService,
    private usersService: UsersService,
  ) { }

  ngOnInit() {
    this.ordersService.getCountPerDay(5).subscribe(this.processOrderCounts.bind(this))
    this.usersService.getCountPerDay(5).subscribe(this.processUsersCounts.bind(this))
  }

  public ordersLineChartData: ChartConfiguration<'line'>['data'] | undefined
  public usersLineChartData: ChartConfiguration<'line'>['data'] | undefined

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

  processUsersCounts(counts: Map<number, number>) {
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

    this.usersLineChartData = {
      labels: last5Days.map(h => h.getDate()),
      datasets: [
        {
          data: data,
          label: 'New users per day',
          fill: true,
          tension: 0.5,
          borderColor: 'black',
        }
      ]
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

    this.ordersLineChartData = {
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
