const Joi = require('joi');
const { completePublication } = require("../../domain/usecases/complete-publication");

const register = async function(server) {
  server.route([{
    method: 'POST',
    path: '/complete-publication',
    handler: completePublicationHandler,
    options: {
      auth: 'jwt',
      validate: {
        payload: Joi.object({
          makeDataPublic: Joi.boolean()
        })
      }
    }
  }]);
};

const completePublicationHandler = async function (request, h) {
  await completePublication(request.auth.credentials.user.canteenId, request.payload.makeDataPublic);

  return h.response().code(204);
};

module.exports = {
  register,
  completePublicationHandler
};
