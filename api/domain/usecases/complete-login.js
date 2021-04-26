const { getUserForLoginToken } = require("../../infrastructure/repositories/login-token");
const jwt = require("jsonwebtoken");
require('dotenv').config();

exports.generateJWTokenForUser = async function(loginTokenString) {
  let user = await getUserForLoginToken(loginTokenString);
  if(user) {
    return jwt.sign({ email: user.email }, process.env.JWT_SECRET_KEY, { expiresIn: '7 days' });
  }
};
