const _ = require('lodash');
const { sendEmail } = require('../services/mailer');

exports.subscribeBetaTester = async function(betaTester) {
  // TODO: better way of generating html string (ejs.renderFile ?)
  const htmlBody = `<!DOCTYPE html> <html> <body>` +
                    `<p><b>Cantine:</b> ${_.escape(betaTester.school)}</p>` +
                    `<p><b>Ville:</b> ${_.escape(betaTester.city)}</p>` +
                    `<p><b>Email:</b> ${_.escape(betaTester.email)}</p>` +
                    `<p><b>Téléphone:</b> ${_.escape(betaTester.phone || '')}</p>` +
                    `<p><b>Message:</b></p>` +
                    `<p>${_.escape(betaTester.message || '')}</p>` +
                    `</body> </html>`;

  return sendEmail([{ email: process.env.SENDINBLUE_CONTACT_EMAIL }], "Nouveau Béta-testeur ma cantine", htmlBody);
}
