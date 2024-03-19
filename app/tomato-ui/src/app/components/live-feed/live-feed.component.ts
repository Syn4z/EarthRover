import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { TakePictureDialogComponent } from '../take-picture-dialog/take-picture-dialog.component';
import { HttpClient } from '@angular/common/http';
import { interval } from 'rxjs';
import { startWith, switchMap, retryWhen, delay, tap } from 'rxjs/operators';

@Component({
  selector: 'app-live-feed',
  templateUrl: './live-feed.component.html',
  styleUrls: ['./live-feed.component.scss']
})
export class LiveFeedComponent {
  liveImgSrc = '../../../assets/img/loading.gif';

  constructor(public dialog: MatDialog, 
              private http: HttpClient) { }

    ngOnInit() {
    interval(5000)
      .pipe(
        startWith(0), // to make the first request immediately
        switchMap(() => this.http.get('http://127.0.0.1:5000/live', { responseType: 'blob' })),
        retryWhen(errors => errors.pipe(
          tap(error => {
            if (error.status === 404) {
              this.liveImgSrc = '../../../assets/img/loading.gif';
            }
          }),
          delay(5000)
        ))
      )
      .subscribe(
        response => {
          const reader = new FileReader();
          reader.onloadend = () => {
            this.liveImgSrc = reader.result as string;
          };
          if (response) {
            reader.readAsDataURL(response);
          }
        },
        error => {
          if (error.status === 404) {
            this.liveImgSrc = '../../../assets/img/loading.gif';
          }
        }
      );
  }  

  changeImgSrc() {
    this.liveImgSrc = '../../../assets/img/loading.gif';
  }


  openDialog() {
    this.dialog.open(TakePictureDialogComponent, {
      disableClose: true
    });
  }
}
