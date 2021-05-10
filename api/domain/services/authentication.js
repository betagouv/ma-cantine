require('dotenv').config();
const crypto = require('crypto');
const Jwt = require('@hapi/jwt');
const { sendTransactionalEmail } = require("./mailer");
const { saveLoginTokenForUser } = require('../../infrastructure/repositories/login-token')

function generateToken() {
  return crypto.randomBytes(200).toString('base64').slice(0, 255);
};

function generateJwtForUser(user) {
  return Jwt.token.generate({ email: user.email }, process.env.JWT_SECRET_KEY);
};

async function sendLoginLink(user, urlPrefix) {
  const token = generateToken();
  // wait to make sure token is saved successfully before it is sent
  await saveLoginTokenForUser(user, token);

  return sendTransactionalEmail([{ email: user.email }], Number.parseInt(process.env.SENDINBLUE_TEMPLATE_LOGIN, 10), {
    LOGIN_LINK: urlPrefix + encodeURIComponent(token)
  });
};

function sendSignUpLink(email) {
  return sendTransactionalEmail([{ email }], Number.parseInt(process.env.SENDINBLUE_TEMPLATE_SIGN_UP, 10));
};

module.exports = {
  sendLoginLink,
  sendSignUpLink,
  generateJwtForUser
}