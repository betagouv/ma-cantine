const Joi = require('joi');
const { signUp } = require("../../domain/usecases/sign-up");

const signUpHandler = async function(request, h) {
  const { user, canteen, loginUrl } = request.payload;
  await signUp(user, canteen, loginUrl);
  return h.response().code(200);
};

const register = async function(server) {
  server.route([{
    method: "POST",
    path: "/sign-up",
    handler: signUpHandler,
    options: {
      validate: {
        payload: Joi.object({
          user: Joi.object({
            firstName: Joi.string().required(),
            lastName: Joi.string().required(),
            email: Joi.string().email().required()
          }),
          canteen: Joi.object({
            name: Joi.string().required(),
            city: Joi.string().required(),
            sector: Joi.string().required(),
            siret: Joi.string().allow('', null),
            managementType: Joi.string().required()
          }),
          loginUrl: Joi.string().uri().required()
        })
      }
    }
  }]);
};

module.exports = {
  signUpHandler,
  register
};