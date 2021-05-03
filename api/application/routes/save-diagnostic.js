// example auth route for now - to be replaced by real save diagnostic endpoint
const saveDiagnosticHandler = async function(request, h) {
  return h.response({ id: request.auth.credentials.user.id }).code(200);
};

exports.register = async function(server) {
  server.route([{
    method: "GET",
    path: "/save-diagnostic",
    handler: saveDiagnosticHandler,
    options: {
      auth: 'jwt'
    }
  }]);
};
