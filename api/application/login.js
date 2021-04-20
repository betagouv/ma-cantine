const { saveTokenForUser, getUserForLoginToken } = require("../infrastructure/repositories/login-token");
const { findUser } = require('../infrastructure/repositories/user');
const { sendSignUpLink } = require('./sign-up');
const fetch = require('node-fetch');
const crypto = require('crypto');
const jwt = require("jsonwebtoken");
require('dotenv').config();

function generateToken() {
  return crypto.randomBytes(256).toString('base64');
};

// TODO: consider writing sendMail util, pro is both conciseness and making it more sendinblue agnostic
// can then also put escaping in the one place
function sendLoginLink(email, token) {
  const loginEmailRequest = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "api-key": undefined
    },
    body: JSON.stringify({
      sender: { email: undefined, name: "Site web ma cantine" },
      to: [{ email: email }],
      replyTo: { email: undefined },
      subject: "Votre lien de connexion avec ma cantine",
      // TODO: better way of generating html string (ejs.renderFile ?)
      htmlContent: "<!DOCTYPE html> <html> <body>"+
                   "<a href='?token="+encodeURIComponent(token)+">Connectez-moi</a>"+
                    "</body> </html>"
    })
  }
  fetch("https://api.sendinblue.com/v3/smtp/email", loginEmailRequest);
};

async function initiateMagicLinkLogin(email) {
  let user = await findUser({ email: email });
  if(user) {
    const token = generateToken();
    // wait to make sure token is saved successfully before it is sent
    await saveTokenForUser(user, token);
    sendLoginLink(email, token);
  } else {
    sendSignUpLink(email);
    return;
  }
};

async function generateJWTokenForUser(loginTokenString) {
  let user = await getUserForLoginToken(loginTokenString);
  if(user) {
    return jwt.sign({ email: user.email }, process.env.JWT_SECRET_KEY, { expiresIn: '7 days' });
  }
};

module.exports = {
  initiateMagicLinkLogin,
  generateJWTokenForUser
};