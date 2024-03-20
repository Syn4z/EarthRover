import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-take-picture-dialog',
  templateUrl: './take-picture-dialog.component.html',
  styleUrls: ['./take-picture-dialog.component.scss']
})
export class TakePictureDialogComponent {
  dialogTitle = '💥 Taking the picture';

  constructor(public dialogRef: MatDialogRef<TakePictureDialogComponent>,
              private http: HttpClient) { }

  ngOnInit() {
    setTimeout(() => {
      this.dialogTitle = '🧠 Analyzing the image';
    }, 2000);

    setTimeout(() => {
      this.dialogTitle = '✅ Getting the results';
    }, 5000);

    setTimeout(() => {
      this.sendDiseaseData().subscribe(() => {
        console.log('Disease data sent');
      });
      this.dialogRef.close();
    }, 7000);
  }

  sendDiseaseData() {
    const diseaseData = {
      "id": 0,
      "name": "Healthy",
      "description": "No disease detected",
      "confidence": 98,
      "date": "March, 2024",
      "image": "assets/img/healthy.jpg",
      "treatment": []
    };

    return this.http.post('http://127.0.0.1:5000/disease', diseaseData);
  }
}
