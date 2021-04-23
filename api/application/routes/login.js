const Joi = require('joi');
const { initiateLogin, completeLogin } = require('../controllers/login');

exports.register = async function(server) {
  server.route([
    {
      method: "POST",
      path: "/login",
      handler: initiateLogin,
      options: {
        validate: {
          payload: Joi.object({
            email: Joi.string().email().required()
          })
        }
      }
    },
    {
      method: "GET",
      path: "/complete-login",
      handler: completeLogin,
      options: {
        validate: {
          query: Joi.object({
            token: Joi.string().required()
          })
        }
      }
    }
    // test user data link for authentication?
  ]);
};
