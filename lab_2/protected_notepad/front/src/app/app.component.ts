import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {take} from 'rxjs/operators';
import * as keypair from 'keypair';
import * as NodeRSA from 'node-rsa';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  private readonly url: string = '/api/';
  fileNameInput = 'file.txt';
  text = '';
  sessionKey = '';
  rsaPair;

  constructor(private httpClient: HttpClient) {
  }

  ngOnInit(): void {
  }

  generateOpenPartRSA(): void {
    this.rsaPair = keypair();
    this.httpClient.post(this.url + 'set-open-rsa', {openPart: this.rsaPair.public})
      .pipe(take(1))
      .subscribe();
  }

  generateSessionKey(): void {
    this.httpClient.get(this.url + 'session-key', {responseType: 'text'})
      .pipe(take(1))
      .subscribe((sessionKey: any) => {
        const key = new NodeRSA(this.rsaPair.public);
        const generatedKey = key.decrypt(sessionKey);
        this.sessionKey = generatedKey;
      });
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
