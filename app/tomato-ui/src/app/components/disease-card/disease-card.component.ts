import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-disease-card',
  templateUrl: './disease-card.component.html',
  styleUrls: ['./disease-card.component.scss']
})
export class DiseaseCardComponent {
  @Input() disease: any;  
}