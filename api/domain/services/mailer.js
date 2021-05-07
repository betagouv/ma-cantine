const fetch = require('node-fetch');

const sendEmail = function(to, subject, html) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "api-key": process.env.SENDINBLUE_API_KEY },
    body: JSON.stringify({
      sender: { email: process.env.SENDINBLUE_SENDER_EMAIL, name: process.env.SENDINBLUE_SENDER_NAME },
      to,
      replyTo: { email: process.env.SENDINBLUE_CONTACT_EMAIL },
      subject,
      htmlContent: html
    })
  }
  return fetch("https://api.sendinblue.com/v3/smtp/email", requestOptions);
};

const sendTransactionalEmail = function(to, templateId, params) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "api-key": process.env.SENDINBLUE_API_KEY },
    body: JSON.stringify({ to, templateId, params })
  }
  return fetch("https://api.sendinblue.com/v3/smtp/email", requestOptions);
};

module.exports = {
  sendEmail,
  sendTransactionalEmail
}