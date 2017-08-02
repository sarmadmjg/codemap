let express = require('express');
let app = express();

let apiRouter = require('./api');

app.use('/api', apiRouter);

app.use('/', express.static('static'));

app.listen(80);