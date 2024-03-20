import { Component } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'tomato-ui';
  constructor(private translate: TranslateService) {
    translate.setDefaultLang('ro');
  }

  switchLanguage(language: string) {
    this.translate.use(language);
  }
}
