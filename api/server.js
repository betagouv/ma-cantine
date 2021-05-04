'use strict';
require('dotenv').config();
const Hapi = require('@hapi/hapi');
const Jwt = require('@hapi/jwt');
const glob = require('glob');
const path = require('path');
const { NotFoundError } = require('./infrastructure/errors');
const { getUserByEmail } = require('./infrastructure/repositories/user');

const server = Hapi.server({
  host: process.env.HOST || 'localhost',
  port: process.env.PORT || 3000,
  routes: {
    cors: {
      origin: ['*']
    }
  },
  debug: {
    request: ['error']
  }
});

// development logging
if(process.env.NODE_ENV !== 'test') {
  server.events.on('response', function (request) {
    console.log(request.info.remoteAddress + ': ' + request.method.toUpperCase() + ' ' + request.path + ' ' + JSON.stringify(request.payload) + ' --> ' + request.response.statusCode);
  });
}

const prepareServer = async function(server) {
  await server.register(Jwt);
  server.auth.strategy('jwt', 'jwt', {
    keys: process.env.JWT_SECRET_KEY,
    verify: {
      aud: false,
      iss: false,
      sub: false,
      nbf: true,
      exp: true,
      maxAgeSec: 7 * 24 * 60 * 60, // 7 days
      timeSkewSec: 15
    },
    validate: async (artifacts, request, h) => {
      // TODO: getting the front-end to store token in localstorage is non-ideal
      // use cookies instead? - in request.state to fetch then parse and validate token
      let user;
      try {
        user = await getUserByEmail(artifacts.decoded.payload.email);
      } catch(e) {
        if(e instanceof NotFoundError) {
          return { isValid: false };
        } else {
          throw e;
        }
      }
      return {
        isValid: true,
        credentials: { user }
      };
    }
  });

  // Look through the routes and register each
  glob.sync('./application/routes/*.js', { 
    root: __dirname 
  }).forEach(file => {
    const route = require(path.join(__dirname, file));
    route.register(server);
  });
};

exports.init = async () => {
  await prepareServer(server);
  await server.initialize();
  return server;
};

exports.start = async () => {
  await prepareServer(server);
  await server.start();
  console.log(`Server running at: ${server.info.uri}`);
  return server;
};

process.on('unhandledRejection', (err) => {
  console.log(err);
  process.exit(1);
});
