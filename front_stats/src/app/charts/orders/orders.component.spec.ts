import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartOrdersComponent } from './orders.component';

describe('OrdersComponent', () => {
  let component: ChartOrdersComponent;
  let fixture: ComponentFixture<ChartOrdersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChartOrdersComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChartOrdersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
