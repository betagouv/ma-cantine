const Joi = require('joi');
const { initiateLogin } = require("../../domain/usecases/initiate-login");

const handler = async function (request, h) {
  await initiateLogin(request.payload.email, request.payload.loginUrl);
  return h.response().code(200);
};

exports.register = async function(server) {
  server.route([
    {
      method: "POST",
      path: "/login",
      handler,
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
