import { Component } from '@angular/core';
import diseases from '../../data/diseases.json';
import { MatSelectChange } from '@angular/material/select';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment.development';

@Component({
  selector: 'app-disease-card-list',
  templateUrl: './disease-card-list.component.html',
  styleUrls: ['./disease-card-list.component.scss']
})
export class DiseaseCardListComponent {
  diseases: any = diseases;
  endpoint = environment.apiUrl + '/image';
  local_endpoint = environment.localApiUrl + '/image';
  selectedValue: string = 'all';
  selectedCar!: string;
  intervalId: any;

  months: any[] = [
    {value: 'all', viewValue: 'All'},
    {value: 'April, 2024', viewValue: 'April'},
    {value: 'March, 2024', viewValue: 'March'},
    {value: 'February, 2024', viewValue: 'February'},
    {value: 'January, 2024', viewValue: 'January'},
  ];

  months_compare: any = {
    'January, 2024': 1,
    'February, 2024': 2,
    'March, 2024': 3,
    'April, 2024': 4,
  }; 

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Sort diseases by month, from latest to earliest
    this.diseases.sort((a: any, b: any) => {
      return this.months_compare[b.date] - this.months_compare[a.date];
    });

    // Sort by timestamp, from latest to earliest
    this.diseases.sort((a: any, b: any) => {
      return b.timestamp - a.timestamp;
    });

    this.intervalId = setInterval(() => {
      this.http.get(this.endpoint).subscribe((res:any) => {
        console.log("GET all images", res);
        // console.log(res.images);
        this.http.post<any>(this.local_endpoint, res.images).subscribe((data) => {
          console.log("POST all images", data);
        });
      });
    }, 5000);
  }

  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
  
  onSelectionChange(event: MatSelectChange) {
    this.selectedValue = event.value;
  }
}