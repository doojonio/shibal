import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartOperationsTypesComponent } from './operations-types.component';

describe('OperationsTypesComponent', () => {
  let component: ChartOperationsTypesComponent;
  let fixture: ComponentFixture<ChartOperationsTypesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChartOperationsTypesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChartOperationsTypesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
