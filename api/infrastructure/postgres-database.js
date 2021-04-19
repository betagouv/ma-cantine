require('dotenv').config();
const { Sequelize } = require('sequelize');

// Jest sets NODE_ENV to test if it is undefined
const DATABASE_URL = (process.env.NODE_ENV === 'test') ? process.env.TEST_DATABASE_URL : process.env.DATABASE_URL;

exports.sequelize = new Sequelize(DATABASE_URL);
