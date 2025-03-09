import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartTotalCuttedComponent } from './total-cutted.component';

describe('TotalCuttedComponent', () => {
  let component: ChartTotalCuttedComponent;
  let fixture: ComponentFixture<ChartTotalCuttedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChartTotalCuttedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChartTotalCuttedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
