const Joi = require('joi');
const { generateJWTokenForUser } = require("../../domain/usecases/complete-login");

const completeLogin = async function(request, h) {
  // buffer for email crawlers ?
  let response, code;
  const jwt = await generateJWTokenForUser(request.query.token);
  if(jwt) {
    response = { jwt };
    code = 200;
  } else {
    code = 400;
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
