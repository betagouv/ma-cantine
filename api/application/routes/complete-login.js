const Joi = require('joi');
const { generateJWTokenForUser } = require("../../domain/usecases/complete-login");
const { NoLoginTokenError } = require("../../domain/errors");

const completeLogin = async function(request, h) {
  // buffer for email crawlers ?
  let response, code;
  try {
    const jwt = await generateJWTokenForUser(request.query.token);
    response = { jwt };
    code = 200;
  } catch(e) {
    if(e instanceof NoLoginTokenError) {
      code = 400;
    } else {
      throw e;
    }
  }
  // do something with token?
  // log within functions so reason shows up in sclaingo for debugging?
  return h.response(response).code(code);
};

exports.register = async function(server) {
  server.route([
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
  ]);
};
