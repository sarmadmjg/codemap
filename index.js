const express = require('express');
const app = express();

const db = require('./db_setup');
const Category = db.Category;
const User = db.User;
const Entry = db.Entry;

let apiRouter = require('./api');

app.use('/api', apiRouter);

app.use('/static', express.static('static'));

app.listen(80);
