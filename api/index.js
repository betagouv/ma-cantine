'use strict';
require('dotenv').config();
const Hapi = require('@hapi/hapi');
const betaTester = require('./application/beta-tester.js');

const init = async () => {
  const server = Hapi.server({
    port: 3000,
    host: 'localhost',
    routes: {
      cors: {
        origin: ['*'] // an array of origins or 'ignore'
      }
    }
  });

  betaTester.register(server);

  await server.start();
    console.log('Server running on %s', server.info.uri);
  };

  process.on('unhandledRejection', (err) => {

  console.log(err);
  process.exit(1);
});

init();