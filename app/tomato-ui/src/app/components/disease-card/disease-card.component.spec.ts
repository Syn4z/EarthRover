import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiseaseCardComponent } from './disease-card.component';

describe('DiseaseCardComponent', () => {
  let component: DiseaseCardComponent;
  let fixture: ComponentFixture<DiseaseCardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DiseaseCardComponent]
    });
    fixture = TestBed.createComponent(DiseaseCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
