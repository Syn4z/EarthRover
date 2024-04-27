import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { TakePictureDialogComponent } from '../take-picture-dialog/take-picture-dialog.component';
import { HttpClient } from '@angular/common/http';
import { GetPictureDialogComponent } from '../get-picture-dialog/get-picture-dialog.component';

@Component({
  selector: 'app-live-feed',
  templateUrl: './live-feed.component.html',
  styleUrls: ['./live-feed.component.scss']
})
export class LiveFeedComponent {
  remoteImgSrc = '../../../assets/img/loading.gif'
  // remoteImgSrc = 'https://192.168.101.99:5000/video_feed';
  liveImgSrc = this.remoteImgSrc;
  intervalId: any;
  
  constructor(public dialog: MatDialog, http: HttpClient) { }
  
  ngOnInit() {
    this.intervalId = setInterval(() => {
      this.liveImgSrc = this.remoteImgSrc + '?timestamp=' + new Date().getTime();
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
