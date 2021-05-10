const fetch = require('node-fetch');

const sendEmailBody = function(body) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "api-key": process.env.SENDINBLUE_API_KEY },
    body: body
  }
  return fetch("https://api.sendinblue.com/v3/smtp/email", requestOptions);
};

const sendEmail = function(to, subject, html) {
  const body = JSON.stringify({
    sender: { email: process.env.SENDINBLUE_SENDER_EMAIL, name: process.env.SENDINBLUE_SENDER_NAME },
    to,
    replyTo: { email: process.env.SENDINBLUE_CONTACT_EMAIL },
    subject,
    htmlContent: html
  });
  return sendEmailBody(body);
};

const sendTransactionalEmail = function(to, templateId, params) {
  return sendEmailBody(JSON.stringify({ to, templateId, params }));
};

module.exports = {
  sendEmail,
  sendTransactionalEmail
}