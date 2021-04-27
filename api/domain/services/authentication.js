const crypto = require('crypto');
const { sendEmail } = require("./mailer");
const { saveLoginTokenForUser } = require('../../infrastructure/repositories/login-token')

function generateToken() {
  return crypto.randomBytes(200).toString('base64').slice(0, 255);
};

async function sendLoginLink(user, urlPrefix) {
  const token = generateToken();
  // wait to make sure token is saved successfully before it is sent
  await saveLoginTokenForUser(user, token);
  // TODO: better way of generating html string (ejs.renderFile/send in blue templates ?)
  const htmlBody = `<!DOCTYPE html> <html> <body>`+
                   `<p><a href='${urlPrefix + encodeURIComponent(token)}'>Connectez-moi</a></p>`+
                   `</body> </html>`;

  sendEmail([{ email: user.email }], "Votre lien de connexion avec ma cantine", htmlBody)
};

function sendSignUpLink(email) {
  const htmlBody = `<!DOCTYPE html> <html> <body>`+
                   `<p>Une personne a essayé de connecter avec cette adresse email, mais nous n'avons pas trouvé un compte afilié.</p>`+
                   `<p>Si vous voulez créer un compte, visitez-nous a <a href='https://ma-cantine.beta.gouv.fr'>ma-cantine.beta.gouv.fr</a>.</p>`+
                   `<p>Sinon, vous pouvez ignorer ce message.</p>`+
                   `</body> </html>`;
  sendEmail([{ email }], "Demande de connexion avec ma cantine", htmlBody);
};

module.exports = {
  sendLoginLink,
  sendSignUpLink
}