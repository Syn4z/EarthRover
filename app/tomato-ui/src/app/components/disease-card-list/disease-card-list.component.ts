import { Component } from '@angular/core';
import diseases from '../../data/diseases.json';
import { MatSelectChange } from '@angular/material/select';

@Component({
  selector: 'app-disease-card-list',
  templateUrl: './disease-card-list.component.html',
  styleUrls: ['./disease-card-list.component.scss']
})
export class DiseaseCardListComponent {
  diseases: any = diseases;
  random!: SeededRandom;

  selectedValue: string = 'all';
  selectedCar!: string;

  months: any[] = [
    {value: 'all', viewValue: 'All'},
    {value: 'March, 2024', viewValue: 'March'},
    {value: 'February, 2024', viewValue: 'February'},
    {value: 'January, 2024', viewValue: 'January'},
  ];
  
  ngOnInit() {
    this.random = new SeededRandom(123);
    
    // Shuffle the diseases array
    for (let i = this.diseases.length - 1; i > 0; i--) {
      const j = Math.floor(this.random.nextFloat() * (i + 1));
      [this.diseases[i], this.diseases[j]] = [this.diseases[j], this.diseases[i]];
    }
  }

  onSelectionChange(event: MatSelectChange) {
    this.selectedValue = event.value;
  }
}

class SeededRandom {
  constructor(private seed = 123456789) {
    this.seed = seed % 2147483647;
    if (this.seed <= 0) this.seed += 2147483646;
  }

  next() {
    return this.seed = this.seed * 16807 % 2147483647;
  }

  nextFloat() {
    // We know that result of next() will be 1 to 2147483646 (inclusive).
    return (this.next() - 1) / 2147483646;
  }
}