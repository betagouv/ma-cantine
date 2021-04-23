const Joi = require('joi');
const { subscribeBetaTester } = require('../controllers/subscribe-beta-tester');

const JoiSubMeasure = Joi.object({
  shortTitle: Joi.string().required(),
  status: Joi.string()
});

const JoiKeyMeasure = Joi.object({
  shortTitle: Joi.string().required(),
  subMeasures: Joi.array().required().items(JoiSubMeasure)
});

exports.register = async function(server) {
  server.route([{
    method: 'POST',
    path: '/subscribe-beta-tester',
    handler: subscribeBetaTester,
    options: {
      validate: {
        payload: Joi.object({
          keyMeasures: Joi.array().required().items(JoiKeyMeasure),
          form: Joi.object({
            email: Joi.string().email().required(),
            school: Joi.string(),
            city: Joi.string(),
            phone: Joi.string(),
            message: Joi.string()
          })
        })
      }
    }
  }]);
}
