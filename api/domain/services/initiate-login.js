const crypto = require('crypto');
const { sendEmail } = require("./send-email");
const { findUser } = require('../../infrastructure/repositories/user');
const { saveLoginTokenForUser } = require('../../infrastructure/repositories/login-token');

function generateToken() {
  // TODO: test adding a string of the length generated here, how many bytes? originally 256
  return crypto.randomBytes(50).toString('base64');
};

function sendLoginLink(email, token, urlPrefix) {
  // TODO: better way of generating html string (ejs.renderFile/send in blue templates ?)
  const htmlBody = `<!DOCTYPE html> <html> <body>`+
                   `<p><a href='${urlPrefix + encodeURIComponent(token)}'>Connectez-moi</a></p>`+
                   `</body> </html>`;

  sendEmail([{ email }], "Votre lien de connexion avec ma cantine", htmlBody)
};

function sendSignUpLink(email) {
  const htmlBody = `<!DOCTYPE html> <html> <body>`+
                   `<p>Une personne a essayé de connecter avec cette adresse email, mais nous n'avons pas trouvé un compte afilié.</p>`+
                   `<p>Si vous voulez créer un compte, visitez-nous a <a href='https://ma-cantine.beta.gouv.fr'>ma-cantine.beta.gouv.fr</a>.</p>`+
                   `<p>Sinon, vous pouvez ignorer ce message.</p>`+
                   `</body> </html>`;
  sendEmail([{ email }], "Demande de connexion avec ma cantine", htmlBody);
};

async function initiateMagicLinkLogin(email, completeLoginUrl) {
  let user = await findUser({ email: email });
  if(user) {
    const token = generateToken();
    // wait to make sure token is saved successfully before it is sent
    await saveLoginTokenForUser(user, token);
    sendLoginLink(email, token, completeLoginUrl);
  } else {
    sendSignUpLink(email);
  }
};

module.exports = {
  initiateMagicLinkLogin
}