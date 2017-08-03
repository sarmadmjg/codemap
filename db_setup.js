const Sequelize = require('sequelize');
const sequelize = new Sequelize(`sqlite://codemap.db`);

// Category table
let Category = sequelize.define('category', {
    name: {
        type: Sequelize.STRING,
        primaryKey: true
    },
    long_name: { type: Sequelize.STRING },
    description: { type: Sequelize.STRING },
},
{
    timestamps: false,
    freezeTableName: true
});

// User Table
let User = sequelize.define('user', {
    uid: {
        type: Sequelize.STRING,
        primaryKey: true
    },
    name: { type: Sequelize.STRING },
    email: { type: Sequelize.STRING },
},
{
    timestamps: false,
    freezeTableName: true
});

// Entry Table
let Entry = sequelize.define('entry', {
    name: { type: Sequelize.STRING },
    description: { type: Sequelize.STRING },
    link: { type: Sequelize.STRING }
},
{
    timestamps: false,
    freezeTableName: true
});

// Forgein Key realtionships
Entry.belongsTo(User);
Entry.belongsTo(Category);

module.exports = {
    'User': User,
    'Category': Category,
    'Entry': Entry
};
