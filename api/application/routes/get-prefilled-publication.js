const { getPrefilledPublication } = require("../../domain/usecases/get-prefilled-publication");

const register = async function(server) {
  server.route([{
    method: "GET",
    path: "/get-prefilled-publication",
    handler: getPrefilledPublicationHandler,
    options: {
      auth: 'jwt'
    }
  }]);
};

const getPrefilledPublicationHandler = async function(request, h) {
  const prefilledPublication = await getPrefilledPublication(request.auth.credentials.user.canteenId);

  return h.response(prefilledPublication).code(200);
};

module.exports = {
  register,
  getPrefilledPublicationHandler
};
