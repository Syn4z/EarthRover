import { Component } from '@angular/core';
import diseases from '../../data/diseases.json';

@Component({
  selector: 'app-numbers',
  templateUrl: './numbers.component.html',
  styleUrls: ['./numbers.component.scss'],
})
export class NumbersComponent {
  diseases: any = diseases;
  healthyCount: number = this.diseases.filter(
    (disease: any) => disease.name === 'Healthy'
  ).length;
  infectedCount: number = this.diseases.filter(
    (disease: any) => disease.name !== 'Healthy'
  ).length;
  diseaseTypesAll: string[] = [
    'Healthy',
    'Scorch',
    'Nitrogen Deficiency',
    'Potassium Deficiency',
    'Calcium Deficiency',
    'Phytotoxicity',
    'Bacterial Spot',
    'Early Blight',
    'Late Blight',
    'Leaf Mold',
    'Mosaic Virus',
    'Septoria Leaf Spot',
    'Target Spot',
  ];
  diseaseTypes: { type: string; count: number }[] = this.diseaseTypesAll
    .map((diseaseType) => {
      const count = this.diseases.filter(
        (disease: any) => disease.name === diseaseType
      ).length;
      return { type: diseaseType, count };
    })
    .filter((diseaseType) => diseaseType.count > 0)
    .filter((diseaseType) => diseaseType.type !== 'Healthy');
}
