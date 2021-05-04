require('dotenv').config();
const jwt = require("jsonwebtoken");
const { getUserForLoginToken } = require("../../infrastructure/repositories/login-token");

exports.completeLogin = async function(loginTokenString) {
  let user = await getUserForLoginToken(loginTokenString);
  return {
    jwt: jwt.sign({ email: user.email }, process.env.JWT_SECRET_KEY, { expiresIn: '7 days' })
  };
};
