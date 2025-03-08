import { Component, Input } from '@angular/core';
import { Operation, OperationsService } from '../../services/operations.service';
import { MatTableModule } from '@angular/material/table';
import { DatePipe, DecimalPipe, JsonPipe } from '@angular/common';
import { OpTypePipe } from '../../pipes/op-type.pipe';

@Component({
  selector: 'app-tables-operations',
  imports: [
    MatTableModule,
    DatePipe,
    DecimalPipe,
    JsonPipe,
    OpTypePipe,
  ],
  templateUrl: './operations.component.html',
  styleUrl: './operations.component.scss'
})
export class TableOperationsComponent {
  @Input() userId: string | undefined
  displayedColumns = ['id', 'op_type', 'started', 'took', 'details']
  operations: Operation[] = []

  constructor(
    private operationsService: OperationsService,
  ) { }

  ngOnInit() {
    this.operationsService.getOperations(this.userId).subscribe(ops => { this.operations = ops })
  }

}
