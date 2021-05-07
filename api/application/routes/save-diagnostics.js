const Joi = require('joi');
const { JoiDiagnostic } = require('../validation');
const { saveDiagnosticsForCanteen } = require('../../domain/usecases/save-diagnostics');

const saveDiagnosticsHandler = async function(request, h) {
  await saveDiagnosticsForCanteen(request.auth.credentials.user.canteenId, request.payload.diagnostics);
  return h.response().code(201);
};

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