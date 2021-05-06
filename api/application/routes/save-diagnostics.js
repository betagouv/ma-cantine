const Joi = require('joi');
const { saveDiagnosticsForCanteen } = require('../../domain/usecases/save-diagnostics');

const saveDiagnosticsHandler = async function(request, h) {
  await saveDiagnosticsForCanteen(request.auth.credentials.user.canteenId, request.payload.diagnostics);
  return h.response().code(201);
};

const JoiDiagnostic = Joi.object({
  year: Joi.number().integer().min(2000).required(),
  valueBio: Joi.number().min(0),
  valueFairTrade: Joi.number().min(0),
  valueSustainable: Joi.number().min(0),
  valueTotal: Joi.number().min(0),
  hasMadeWasteDiagnostic: Joi.boolean(),
  hasMadeWastePlan: Joi.boolean(),
  wasteActions: Joi.array().items(Joi.string()),
  hasDonationAgreement: Joi.boolean(),
  hasMadeDiversificationPlan: Joi.boolean(),
  vegetarianFrequency: Joi.string(),
  vegetarianMenuType: Joi.string(),
  cookingFoodContainersSubstituted: Joi.boolean(),
  serviceFoodContainersSubstituted: Joi.boolean(),
  waterBottlesSubstituted: Joi.boolean(),
  disposableUtensilsSubstituted: Joi.boolean(),
  communicationSupports: Joi.array().items(Joi.string()),
  communicationSupportLink: Joi.string(),
  communicateOnFoodPlan: Joi.boolean()
});

const register = async function(server) {
  server.route([{
    method: "POST",
    path: "/save-diagnostics",
    handler: saveDiagnosticsHandler,
    options: {
      auth: 'jwt',
      validate: {
        payload: Joi.object({
          diagnostics: Joi.array().items(JoiDiagnostic).required()
        })
      }
    }
  }]);
};

module.exports = {
  register,
  saveDiagnosticsHandler
};