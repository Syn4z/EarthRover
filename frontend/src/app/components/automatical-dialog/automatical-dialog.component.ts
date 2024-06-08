import { Component } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-automatical-dialog',
  templateUrl: './automatical-dialog.component.html',
  styleUrls: ['./automatical-dialog.component.scss']
})
export class AutomaticalDialogComponent {
  dotsDict: any = {
    1: '.',
    2: '..',
    3: '...',
    4: '....',
    5: '.....',
  }; 
  currentStatus: number = 1;
  dialogTitle: string = '📷 Taking the pictures';  
  dotSuffix = this.dotsDict[this.currentStatus];
  endpoint = environment.raspberryPiUrl + '/take_photo';
  intervalId: any;
  timeoutSeconds: number = 100; 

  constructor(public dialogRef: MatDialogRef<AutomaticalDialogComponent>,
              private http: HttpClient) { }

  ngOnInit() {
    this.intervalId = setInterval(() => {
      this.takePicture().subscribe((res) => {
        console.log(res);
      });
      this.dotSuffix = this.dotsDict[this.currentStatus];
      this.currentStatus = this.currentStatus === 5 ? 1 : this.currentStatus + 1;
    }, 5000);
 
    setTimeout(() => {
      this.dialogRef.close();
    }, this.timeoutSeconds * 1000);
  }

  takePicture() {
    return this.http.post(this.endpoint, {});
  }

  close() {
    this.dialogRef.close();
  }

  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
}
