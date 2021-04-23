const Joi = require('joi');
const { signUp } = require("../controllers/sign-up");

exports.register = async function(server) {
  server.route([{
    method: "POST",
    path: "/sign-up",
    handler: signUp,
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
            sector: Joi.string().required() // TODO: validate from sector list
          })
        })
      }
    }
  }]);
};
