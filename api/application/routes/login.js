const { initiateLogin, completeLogin } = require('../controllers/login');

exports.register = async function(server) {
  server.route([
    {
      method: "POST",
      path: "/login",
      handler: initiateLogin
    },
    {
      method: "GET",
      path: "/complete-login",
      handler: completeLogin,
    }
    // test user data link for authentication?
  ]);
};
