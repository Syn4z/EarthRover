import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TakePictureDialogComponent } from './take-picture-dialog.component';

describe('TakePictureDialogComponent', () => {
  let component: TakePictureDialogComponent;
  let fixture: ComponentFixture<TakePictureDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TakePictureDialogComponent]
    });
    fixture = TestBed.createComponent(TakePictureDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
