const Joi = require('joi');
const { JoiDiagnostic } = require('../validation');
const { completeLogin } = require("../../domain/usecases/complete-login");
const { NotFoundError } = require('../../infrastructure/errors');

const handler = async function(request, h) {
  let response, code;
  try {
    response = await completeLogin(request.payload.token, request.payload.diagnostics);
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
      method: "POST",
      path: "/complete-login",
      handler,
      options: {
        validate: {
          payload: Joi.object({
            token: Joi.string().required(),
            diagnostics: Joi.array().items(JoiDiagnostic)
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