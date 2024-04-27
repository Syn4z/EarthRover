import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-get-picture-dialog',
  templateUrl: './get-picture-dialog.component.html',
  styleUrls: ['./get-picture-dialog.component.scss']
})
export class GetPictureDialogComponent {
  results: any = [];

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.http.get('https://earthrover.azurewebsites.net/photo_analysis').subscribe((data: any) => {
      this.results = data;
    });
  }
}
