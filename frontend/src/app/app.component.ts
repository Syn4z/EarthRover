import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'tomato-ui';
  currentLanguage = 'en';

  constructor(private translate: TranslateService) {
    const storedLanguage = localStorage.getItem('currentLanguage') || 'en';
    translate.setDefaultLang(storedLanguage);
    this.currentLanguage = storedLanguage;
  }

  switchLanguage(language: string) {
    this.translate.use(language);
    this.currentLanguage = language;
    localStorage.setItem('currentLanguage', language);
  }
}
