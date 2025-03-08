import { Component } from '@angular/core';
import { ChartConfiguration, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { ChartOperationsComponent } from '../../charts/operations/operations.component';
import { ChartOrdersComponent } from '../../charts/orders/orders.component';
import { UsersService } from '../../services/users.service';
import { getLastDays } from '../../utils/dates';
import { ChartOperationsTypesComponent } from '../../charts/operations-types/operations-types.component';

@Component({
  selector: 'app-home',
  imports: [BaseChartDirective, ChartOperationsComponent, ChartOrdersComponent, ChartOperationsTypesComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

  constructor(
    private usersService: UsersService,
  ) { }

  ngOnInit() {
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

}
