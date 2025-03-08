import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableOperationsComponent } from './operations.component';

describe('OperationsComponent', () => {
  let component: TableOperationsComponent;
  let fixture: ComponentFixture<TableOperationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TableOperationsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TableOperationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
