const Joi = require("joi");

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

module.exports = {
  JoiDiagnostic
}