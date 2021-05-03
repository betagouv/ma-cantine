const { getUserForLoginToken } = require("../../infrastructure/repositories/login-token");
const { generateJwtForUser } = require("../services/authentication");

exports.completeLogin = async function(loginTokenString) {
  let user = await getUserForLoginToken(loginTokenString);
  return {
    jwt: generateJwtForUser(user)
  };
};
