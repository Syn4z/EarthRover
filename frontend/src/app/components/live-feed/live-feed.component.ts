import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { TakePictureDialogComponent } from '../take-picture-dialog/take-picture-dialog.component';
import { HttpClient } from '@angular/common/http';
import { GetPictureDialogComponent } from '../get-picture-dialog/get-picture-dialog.component';
import { environment } from '../../../environments/environment.development';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-live-feed',
  templateUrl: './live-feed.component.html',
  styleUrls: ['./live-feed.component.scss']
})
export class LiveFeedComponent {
  errorImgSrc = '../../../assets/img/loading.gif';
  remoteImgSrc = environment.raspberryPiUrl + '/video_feed';
  liveImgSrc = this.errorImgSrc;
  intervalId: any;
  
  constructor(public dialog: MatDialog, private http: HttpClient) { }
  
  // ngOnInit() {
  //   this.intervalId = setInterval(() => {
  //     this.liveImgSrc = this.remoteImgSrc + '?timestamp=' + new Date().getTime();
  //   }, 5000);
  // }

  // If this doesn't work, uncomment the above ngOnInit() 
  // and comment out the below ngOnInit()
  ngOnInit() {
    this.intervalId = setInterval(() => {
      this.http.get(this.remoteImgSrc, { responseType: 'blob' }).pipe(
        catchError(error => {
          console.error('Error fetching remote image:', error);
          return of(null);
        })
      ).subscribe(response => {
        if (response !== null) {
          this.liveImgSrc = this.remoteImgSrc + '?timestamp=' + new Date().getTime();
        } else {
          this.remoteImgSrc = this.errorImgSrc;
        }
      });
    }, 5000);
  }

  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  openDialog() {
    this.dialog.open(TakePictureDialogComponent, {
      disableClose: true
    });
  }

  refresh() {
    this.dialog.open(GetPictureDialogComponent, {
      disableClose: false
    });
  }
}
