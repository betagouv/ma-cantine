const Joi = require('joi');
const { subscribeNewsletter } = require("../../domain/usecases/subscribe-newsletter");

const register = async function(server) {
  server.route([{
    method: 'POST',
    path: '/subscribe-newsletter',
    handler: subscribeNewsletterHandler,
    options: {
      validate: {
        payload: Joi.object({
          email: Joi.string().email().required()
        })
      }
    }
  }]);
}

const subscribeNewsletterHandler = async function(request, h) {
  const response = await subscribeNewsletter(request.payload.email);
  const json = await response.json();

  return h.response({ message: json.message }).code(response.status);
};

module.exports = {
  register,
  subscribeNewsletterHandler
};
