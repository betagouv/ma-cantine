const Joi = require('joi');
const { completeLogin } = require("../../domain/usecases/complete-login");
const { NotFoundError } = require('../../infrastructure/errors');

const handler = async function(request, h) {
  let response, code;
  try {
    response = await completeLogin(request.query.token);
    code = 200;
  } catch(e) {
    if(e instanceof NotFoundError) {
      code = 400;
    } else {
      throw e;
    }
  }
  return h.response(response).code(code);
};

const register = async function(server) {
  server.route([
    {
      method: "GET",
      path: "/complete-login",
      handler,
      options: {
        validate: {
          query: Joi.object({
            token: Joi.string().required()
          })
        }
      }
    }
  ]);
};

module.exports = {
  handler,
  register
}