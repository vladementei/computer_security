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



const rsaPair = keypair();
const url = 'http://localhost:8080/';
let sessionKey = '';


document.querySelector('#rsaGenerationBtn').addEventListener('click', () => {
    axios
        .post(url + 'set-open-rsa', {
            openPart: rsaPair.public,
        })
        .then()
        .catch((error) => console.error(error))
});

document.querySelector('#getSessionKeyBtn').addEventListener('click', () => {
    axios
        .get(url + 'session-key')
        .then((res) => {
            const encryptedKey = res.data;
            const decrypter = forge.pki.privateKeyFromPem(rsaPair.private);
            sessionKey = forge.util.decodeUtf8(decrypter.decrypt(forge.util.decode64(encryptedKey)));
            console.log(sessionKey);
        })
        .catch((error) => console.error(error))
})

electron.ipcRenderer.on('openFile', (event, message) => {
    axios
        .get(url + 'file/' + message)
        .then(encryptedFile => {
            document.getElementById('text').value = encryptedFile.data;
        })
        .catch((error) => console.error(error))
});