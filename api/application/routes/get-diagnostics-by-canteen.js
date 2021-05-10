const { getDiagnosticsByCanteen } = require("../../domain/usecases/get-diagnostics-by-canteen");

const getDiagnosticsByCanteenHandler = async function(request, h) {
  const diagnostics = await getDiagnosticsByCanteen(request.auth.credentials.user.canteenId);
  return h.response(diagnostics).code(200);
};

const register = async function(server) {
  server.route([{
    method: "GET",
    path: "/get-diagnostics-by-canteen",
    handler: getDiagnosticsByCanteenHandler,
    options: {
      auth: 'jwt'
    }
  }]);
};

module.exports = {
  register,
  getDiagnosticsByCanteenHandler
};