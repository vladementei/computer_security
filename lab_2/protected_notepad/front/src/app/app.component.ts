import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {RSAOpenPart} from './models.model';
import {take} from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  private readonly url: string = '/api/';
  fileNameInput = 'file.txt';
  text = '';

  constructor(private httpClient: HttpClient) {
  }

  generateOpenPartRSA(): void {
    const rsaOpenPart: RSAOpenPart = {
      e: 100,
      n: 120,
    };
    this.httpClient.post(this.url + 'set-open-rsa', rsaOpenPart)
      .pipe(take(1))
      .subscribe();
  }

  generateSessionKey(): void {
    this.httpClient.get(this.url + 'session-key', {responseType: 'text'})
      .pipe(take(1))
      .subscribe((sessionKey: any) => console.log(sessionKey));
  }

  getFile(): void {
    this.httpClient.get(this.url + 'file/' + this.fileNameInput, {responseType: 'text'})
      .pipe(take(1))
      .subscribe(
        file => this.text = file,
        err => this.text = '',
      );
  }
}
