
require('dotenv').config();
const jwt = require("jsonwebtoken");
const { getUserForLoginToken } = require("../../infrastructure/repositories/login-token");
const { NoLoginTokenError } = require("../errors");

exports.generateJWTokenForUser = async function(loginTokenString) {
  let user = await getUserForLoginToken(loginTokenString);
  if(user) {
    return jwt.sign({ email: user.email }, process.env.JWT_SECRET_KEY, { expiresIn: '7 days' });
  } else {
    throw new NoLoginTokenError();
  }
};
