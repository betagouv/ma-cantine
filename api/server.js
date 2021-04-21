'use strict';
require('dotenv').config();
const Hapi = require('@hapi/hapi');
const login = require('./application/login.js');
const signUp = require('./application/sign-up.js');
const subscribeBetaTester = require('./application/subscribe-beta-tester.js');

const server = Hapi.server({
  host: process.env.HOST || 'localhost',
  port: process.env.PORT || 3000,
  routes: {
    cors: {
      origin: ['*']
    }
  },
  // jwt authentication
  debug: { request: ['error'] }
});

subscribeBetaTester.register(server);
login.register(server);
signUp.register(server);

exports.init = async () => {
  await server.initialize();
  return server;
};

exports.start = async () => {
  await server.start();
  console.log(`Server running at: ${server.info.uri}`);
  return server;
};

process.on('unhandledRejection', (err) => {
  console.log(err);
  process.exit(1);
});
