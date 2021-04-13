require('dotenv').config();
const { Sequelize } = require('sequelize');

// TODO: how to connect to test database when running tests, but prod normally?
exports.sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USERNAME, process.env.DB_PASSWORD, {
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  dialect: 'postgres',
  logging: false // TODO: decide where logs should go
});
