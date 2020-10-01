const express = require('express');
const bodyParser = require('body-parser');
const utils = require('./utils');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));


app.post('/decrypt-text', (request, response) => {
    response.status(200).send(utils.decrypt(request.body.key, request.body.text));
});

app.listen(8180, () => {
    console.log('Server is running on port 8180');
})