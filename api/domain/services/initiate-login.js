const crypto = require('crypto');
const { sendEmail } = require("./send-email");
const { sendSignUpLink } = require('./send-sign-up-link');
const { findUser } = require('../../infrastructure/repositories/user');
const { saveLoginTokenForUser } = require('../../infrastructure/repositories/login-token');

function generateToken() {
  // TODO: test adding a string of the length generated here, how many bytes? originally 256
  return crypto.randomBytes(50).toString('base64');
};

function sendLoginLink(email, token) {
  // TODO: better way of generating html string (ejs.renderFile/send in blue templates ?)
  const htmlBody = `<!DOCTYPE html> <html> <body>`+
                   `<p><a href='${process.env.LOGIN_URL}?token=${encodeURIComponent(token)}'>Connectez-moi</a></p>`+
                   `</body> </html>`;

  sendEmail([{ email }], "Votre lien de connexion avec ma cantine", htmlBody)
};

async function initiateMagicLinkLogin(email) {
  let user = await findUser({ email: email });
  if(user) {
    const token = generateToken();
    // wait to make sure token is saved successfully before it is sent
    await saveLoginTokenForUser(user, token);
    sendLoginLink(email, token);
  } else {
    sendSignUpLink(email);
    return;
  }
};

module.exports = {
  initiateMagicLinkLogin
}