import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';

@Component({
  selector: 'app-take-picture-dialog',
  templateUrl: './take-picture-dialog.component.html',
  styleUrls: ['./take-picture-dialog.component.scss']
})
export class TakePictureDialogComponent {
  dialogTitle = '💥 Taking the picture';
  endpoint = environment.raspberryPiUrl + '/take_photo';

  constructor(public dialogRef: MatDialogRef<TakePictureDialogComponent>,
              private http: HttpClient) { }

  ngOnInit() {
    setTimeout(() => {
      this.takePicture().subscribe((res) => {
        console.log(res);
      });
      this.dialogTitle = '🧠 Analyzing the image';
    }, 2000);

    setTimeout(() => {
      this.dialogTitle = '✅ Getting the results';
    }, 5000);

    setTimeout(() => {
      this.dialogRef.close();
    }, 7000);
  }

  takePicture() {
    return this.http.post(this.endpoint, {});
  }
}
