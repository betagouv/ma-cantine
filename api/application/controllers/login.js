const { initiateMagicLinkLogin, generateJWTokenForUser } = require("../../domain/usecases/login");

const initiateLogin = async function (request, h) {
  initiateMagicLinkLogin(request.payload.email);
  return h.response().code(200);
};

const completeLogin = async function(request, h) {
  // buffer for email crawlers ?
  let response, code;
  const jwt = await generateJWTokenForUser(request.query.token);
  if(jwt) {
    response = { jwt };
    code = 200;
  } else {
    code = 400;
  }
  // do something with token?
  // log within functions so reason shows up in sclaingo for debugging?
  return h.response(response).code(code);
};

module.exports = {
  initiateLogin,
  completeLogin
};