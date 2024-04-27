import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GetPictureDialogComponent } from './get-picture-dialog.component';

describe('GetPictureDialogComponent', () => {
  let component: GetPictureDialogComponent;
  let fixture: ComponentFixture<GetPictureDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GetPictureDialogComponent]
    });
    fixture = TestBed.createComponent(GetPictureDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
