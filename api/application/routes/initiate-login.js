const Joi = require('joi');
const { initiateMagicLinkLogin } = require("../../domain/services/initiate-login");

const initiateLogin = async function (request, h) {
  await initiateMagicLinkLogin(request.payload.email, request.payload.loginUrl);
  return h.response().code(200);
};

exports.register = async function(server) {
  server.route([
    {
      method: "POST",
      path: "/login",
      handler: initiateLogin,
      options: {
        validate: {
          payload: Joi.object({
            email: Joi.string().email().required(),
            loginUrl: Joi.string().uri().required()
          })
        }
      }
    }
  ]);
};
