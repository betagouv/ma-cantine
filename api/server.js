'use strict';
require('dotenv').config();
const Hapi = require('@hapi/hapi');
const initiateLogin = require('./application/routes/initiate-login.js');
const completeLogin = require('./application/routes/complete-login.js');
const signUp = require('./application/routes/sign-up.js');
const subscribeBetaTester = require('./application/routes/subscribe-beta-tester.js');

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

// development logging
if(process.env.NODE_ENV !== 'test') {
  server.events.on('response', function (request) {
    console.log(request.info.remoteAddress + ': ' + request.method.toUpperCase() + ' ' + request.path + ' ' + JSON.stringify(request.payload) + ' --> ' + request.response.statusCode);
  });
}

subscribeBetaTester.register(server);
initiateLogin.register(server);
completeLogin.register(server);
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
