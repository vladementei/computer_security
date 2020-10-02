import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {take} from 'rxjs/operators';
import * as keypair from 'keypair';
import * as forge from 'node-forge';

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
    this.httpClient.post(this.url + 'set-open-rsa', {openPart: this.rsaPair.public, privatePart: this.rsaPair.private})
      .pipe(take(1))
      .subscribe();
  }

  generateSessionKey(): void {
    this.httpClient.get(this.url + 'session-key', {responseType: 'text'})
      .pipe(take(1))
      .subscribe((sessionKey: any) => {
        const decrypter = forge.pki.privateKeyFromPem(this.rsaPair.private);
        this.sessionKey = forge.util.decodeUtf8(decrypter.decrypt(forge.util.decode64(sessionKey)));
        console.log(this.sessionKey);
      });
  }

  getFile(): void {
    this.httpClient.get(this.url + 'file/' + this.fileNameInput, {responseType: 'text'})
      .pipe(take(1))
      .subscribe(
        file => this.text = file,
        err => this.text = ''
      );
  }
}
