const { saveDiagnosticsForCanteen } = require("../../infrastructure/repositories/diagnostic");
const { getUserForLoginToken } = require("../../infrastructure/repositories/login-token");
const { generateJwtForUser } = require("../services/authentication");

exports.completeLogin = async function(loginTokenString, diagnostics) {
  const user = await getUserForLoginToken(loginTokenString);
  await saveDiagnosticsForCanteen(user.canteenId, diagnostics || []);
  return {
    jwt: generateJwtForUser(user)
  };
};
