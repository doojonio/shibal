import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChartConfiguration, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, BaseChartDirective],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'shibal';


  public lineChartData: ChartConfiguration<'line'>['data'] = {
    labels: [
      'Test1',
      'Test2',
      'Test3',
      'Test',
      'Eto',
    ],
    datasets: [
      {
        data: [12, 24, 38, 32, 10],
        label: 'Shit stat',
        fill: true,
        tension: 0.5,
        borderColor: 'black',
        // backgroundColor: 'rgba(255,0,0,0,3)'
      }
    ]
  }

  public lineChartOptions: ChartOptions<'line'> = {
    responsive: false
  }
  public lineChartLegend = true;

  constructor() {}

  ngOnInit() {

  }
}
