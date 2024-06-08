import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AutomaticalDialogComponent } from './automatical-dialog.component';

describe('AutomaticalDialogComponent', () => {
  let component: AutomaticalDialogComponent;
  let fixture: ComponentFixture<AutomaticalDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AutomaticalDialogComponent]
    });
    fixture = TestBed.createComponent(AutomaticalDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
