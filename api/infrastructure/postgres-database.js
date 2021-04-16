require('dotenv').config();
const { Sequelize } = require('sequelize');

// Jest sets NODE_ENV to test if it is undefined
const DB_NAME = (process.env.NODE_ENV === 'test') ? process.env.TEST_DB_NAME : process.env.DB_NAME;

exports.sequelize = new Sequelize(DB_NAME, process.env.DB_USERNAME, process.env.DB_PASSWORD, {
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  dialect: 'postgres',
  logging: false // TODO: decide where logs should go
});
