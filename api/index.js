let express = require('express');
let router = express.Router();

const db = require('../db_setup');
const Category = db.Category;
const User = db.User;
const Entry = db.Entry;

router.get('/', (req, res) => {
    res.end('You reached the api');
});

router.get('/categories', (req, res) => {
    Category.findAll().then(cats => {
        res.json({categories: cats});
    });
});

router.get('/categories/:cat/entries', (req, res) => {
    Entry.findAll({
        where: {
            categoryName: req.params.cat
        }
    }).then(entries => {
        res.json({entries: entries});
    });
});

router.get('/entries/:id', (req, res) => {
    Entry.findOne({
        where: {
            id: req.params.id
        }
    }).then(entry => {
        res.json(entry);
    })
});

module.exports = router;