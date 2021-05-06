const Joi = require('joi');
const { extendCanteenInfos } = require("../../domain/usecases/extend-canteen-infos");

const register = async function(server) {
  server.route([{
    method: 'PATCH',
    path: '/extend-canteen-infos',
    handler: extendCanteenInfosHandler,
    options: {
      auth: 'jwt',
      validate: {
        payload: Joi.object({
          name: Joi.string().required(),
          city: Joi.string().required(),
          sector: Joi.string().required()
        })
      }
    }
  }]);
};

const extendCanteenInfosHandler = async function (request, h) {
  const canteen = {
    id: request.auth.credentials.user.canteenId,
    name: request.payload.name,
    city: request.payload.city,
    sector: request.payload.sector,
  };

  await extendCanteenInfos(canteen);

  return h.response().code(204);
};

module.exports = {
  register,
  extendCanteenInfosHandler
};
