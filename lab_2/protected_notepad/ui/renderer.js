// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.
const keypair = require('keypair');
const electron = require('electron')
const axios = require('axios')
const forge = require('node-forge');
const utils = require('./utils');


const url = 'http://localhost:8080/';


electron.ipcRenderer.on('generateRSA', () => {
    const rsaPair = keypair();
    window.localStorage.setItem('rsa', rsaPair.private);
    axios
        .post(url + 'set-open-rsa', {
            openPart: rsaPair.public,
        })
        .then(() => electron.ipcRenderer.emit('getSessionKey'))
        .catch((error) => console.error(error))
});

electron.ipcRenderer.on('getSessionKey', () => {
    axios
        .get(url + 'session-key')
        .then((res) => {
            const decrypter = forge.pki.privateKeyFromPem(window.localStorage.getItem('rsa'));
            window.localStorage.setItem('sessionKey', forge.util.decodeUtf8(decrypter.decrypt(forge.util.decode64(res.data))));
        })
        .catch((error) => console.error(error))
})

electron.ipcRenderer.on('openFile', (event, message) => {
    window.localStorage.setItem('file', message);
    axios
        .get(url + 'file/' + message)
        .then(encryptedFile => {
            document.getElementById('text').value = utils.decrypt(window.localStorage.getItem('sessionKey'), encryptedFile.data);
        })
        .catch((error) => console.error(error))
});

electron.ipcRenderer.on('saveFile', (event, message) => {
    window.localStorage.setItem('file', message);
    axios
        .post(url + 'file/' + message,
            {text: utils.encrypt(window.localStorage.getItem('sessionKey'), document.getElementById('text').value)})
        .then()
        .catch((error) => console.error(error))
});

electron.ipcRenderer.on('updateFile', () => {
    axios
        .put(url + 'file/' + window.localStorage.getItem('file'),
            {text: utils.encrypt(window.localStorage.getItem('sessionKey'), document.getElementById('text').value)})
        .then()
        .catch((error) => console.error(error))
});

electron.ipcRenderer.on('deleteFile', (event, message) => {
    axios
        .delete(url + 'file/' + message)
        .then()
        .catch((error) => console.error(error))
});

//generate RSA on startup and get session key
electron.ipcRenderer.emit('generateRSA');
