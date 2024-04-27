import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiseaseCardListComponent } from './disease-card-list.component';

describe('DiseaseCardListComponent', () => {
  let component: DiseaseCardListComponent;
  let fixture: ComponentFixture<DiseaseCardListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DiseaseCardListComponent]
    });
    fixture = TestBed.createComponent(DiseaseCardListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
