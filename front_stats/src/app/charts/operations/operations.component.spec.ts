import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartOperationsComponent } from './operations.component';

describe('OperationsComponent', () => {
  let component: ChartOperationsComponent;
  let fixture: ComponentFixture<ChartOperationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChartOperationsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChartOperationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
