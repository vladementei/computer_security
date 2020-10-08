const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const utils = require('./utils');
const forge = require('node-forge');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));


//EXAMPLES
//////////////////////////////////////////////////////////////////////////////////////
app.get('/', (request, response) => {
    response.send('Hello API');
})

app.get('/login', (request, response) => {
    response.send('Login route');
})

app.get('/login/:id', (request, response) => {
    response.send('Login route with id ' + parseInt(request.params.id));
})

app.post('/login', (request, response) => {
    const user = {
        id: request.body.id,
        password: "las"
    }
    response.send(user);
})

app.put('/login/:id', (request, response) => {
    console.log('Login put route with id ' + parseInt(request.params.id));
    console.log(request.body);
    response.sendStatus(200);
})

app.delete('/login/:id', (request, response) => {
    console.log('Login delete route with id ' + parseInt(request.params.id));
    response.sendStatus(200);
})

///////////////////////////////////////////////////////////////////////////

//API

const sessionKey = utils.generateSessionKey();//TODO remove hardcode
let rsaPublicKey = '';//TODO


app.get('/file/:fileName', (request, response) => {
    console.log('Get file ' + request.params.fileName);
    fs.readFile('assets/' + request.params.fileName, 'utf8', (err, contents) => {
        if (!err) {
            response.type('.' + request.params.fileName.split('.').pop());
            response.send(utils.encrypt(sessionKey, contents));
        } else {
            response.sendStatus(404);
        }
    });
    //response.sendFile(__dirname + '/assets/' + request.params.fileName);
});

app.post('/file/:fileName', (request, response) => {
    console.log('Create file ' + request.params.fileName);
    fs.writeFile('assets/' + request.params.fileName,
        utils.decrypt(sessionKey, request.body.text),
        () => {
        });
});

app.put('/file/:fileName', (request, response) => {
    console.log('Update file ' + request.params.fileName);
    fs.writeFile('assets/' + request.params.fileName,
        utils.decrypt(sessionKey, request.body.text),
        () => {
        });
});

app.delete('/file/:fileName', (request, response) => {
    console.log('delete file ' + request.params.fileName);
    fs.unlink('assets/' + request.params.fileName,
        () => {
        });
});

app.get('/session-key', (request, response) => {
    const encrypter = forge.pki.publicKeyFromPem(rsaPublicKey);
    const encryptedSessionKey = forge.util.encode64(encrypter.encrypt(forge.util.encodeUtf8(sessionKey)));
    response.send(encryptedSessionKey);
});

app.post('/set-open-rsa', (request, response) => {
    rsaPublicKey = request.body.openPart;
    console.log('open part = ' + rsaPublicKey);
    response.status(200).send({status: 'OK'});
});


app.listen(8080, () => {
    console.log('Server is running on port 8080');
})