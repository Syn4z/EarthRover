import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DiseaseCardComponent } from './components/disease-card/disease-card.component';
import { DiseaseCardListComponent } from './components/disease-card-list/disease-card-list.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { LiveFeedComponent } from './components/live-feed/live-feed.component';
import { MatDialogModule } from '@angular/material/dialog';
import { TakePictureDialogComponent } from './components/take-picture-dialog/take-picture-dialog.component';
import { HttpClientModule } from '@angular/common/http';
import { StatsComponent } from './components/stats/stats.component';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatTableModule } from '@angular/material/table';

@NgModule({
  declarations: [
    AppComponent,
    DiseaseCardComponent,
    DiseaseCardListComponent,
    LiveFeedComponent,
    TakePictureDialogComponent,
    StatsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatSelectModule,
    MatFormFieldModule,
    FormsModule,
    MatDialogModule,
    HttpClientModule,
    MatProgressSpinnerModule,
    MatPaginatorModule,
    MatTableModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
