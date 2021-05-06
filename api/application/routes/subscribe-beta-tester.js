const Joi = require('joi');
const { subscribeBetaTester } = require("../../domain/usecases/subscribe-beta-tester");

const register = async function(server) {
  server.route([{
    method: 'POST',
    path: '/subscribe-beta-tester',
    handler: subscribeBetaTesterHandler,
    options: {
      validate: {
        payload: Joi.object({
          email: Joi.string().email().required(),
          school: Joi.string(),
          city: Joi.string(),
          phone: Joi.string(),
          message: Joi.string()
        })
      }
    }
  }]);
};

const subscribeBetaTesterHandler = async function(request, h) {
  const response = await subscribeBetaTester(request.payload);
  const json = await response.json();

  return h.response({ message: json.message }).code(response.status);
};

module.exports = {
  register,
  subscribeBetaTesterHandler
};
