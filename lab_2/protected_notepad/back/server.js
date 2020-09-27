const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const utils = require('./utils');

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
app.get('/file/:fileName', (request, response) => {
    console.log('Get file ' + request.params.fileName);
    fs.readFile('assets/' + request.params.fileName, 'utf8', (err, contents) => {
        if (!err) {
            response.type('.' + request.params.fileName.split('.').pop());
            response.send(contents);
        } else {
            response.sendStatus(404);
        }
    });
    //response.sendFile(__dirname + '/assets/' + request.params.fileName);
});

app.get('/session-key', (request, response) => {
    const generatedKey = utils.generateSessionKey();
    response.send(generatedKey);
});

app.post('/set-open-rsa', (request, response) => {
    console.log('e = ' + parseInt(request.body.e));
    console.log('n = ' + parseInt(request.body.n));
    response.sendStatus(200);
});


app.listen(8080, () => {
    console.log('Server is running on port 8080');
})