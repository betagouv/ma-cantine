const { subscribeBetaTester } = require('../controllers/subscribe-beta-tester');

exports.register = async function(server) {
  server.route([{
    method: 'POST',
    path: '/subscribe-beta-tester',
    handler: subscribeBetaTester
  }]);
}
