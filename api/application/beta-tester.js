const _ = require('lodash');
const fetch = require('node-fetch');

exports.register = async function(server) {
  server.route([{
    method: 'POST',
    path: '/subscribe-beta-tester',
    handler: createBetaTester
  }]);
}

async function createBetaTester(request, h) {
  let measuresHtml = '';
  const payload = JSON.parse(request.payload);
  const keyMeasures = payload.keyMeasures;
  keyMeasures.forEach(measure => {
    measuresHtml += `<p><b>${measure.shortTitle} :</b></p>`;
    measure.subMeasures.forEach(subMeasure => {
      // If move key measures to back-end, put back STATUSES[subMeasure.status] to francise
      measuresHtml += `<p>${subMeasure.shortTitle} : ${subMeasure.status || ''}</p>`
    });
  });
  const form = payload.form;
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "api-key": process.env.VUE_APP_SENDINBLUE_API_KEY },
    body: JSON.stringify({
      sender: { email: process.env.VUE_APP_SENDER_EMAIL, name: "site web ma cantine" },
      to: [{ email: process.env.VUE_APP_CONTACT_EMAIL }],
      replyTo: { email: process.env.VUE_APP_CONTACT_EMAIL },
      subject: "Nouveau Béta-testeur ma cantine",
      htmlContent: `<!DOCTYPE html> <html> <body>` +
                   `<p><b>Cantine:</b> ${_.escape(form.school)}</p>` +
                   `<p><b>Ville:</b> ${_.escape(form.city)}</p>` +
                   `<p><b>Email:</b> ${_.escape(form.email)}</p>` +
                   `<p><b>Téléphone:</b> ${_.escape(form.phone || '')}</p>` +
                   `<p><b>Message:</b></p>` +
                   `<p>${_.escape(form.message || '')}</p>` +
                   `${measuresHtml}` +
                   `</body> </html>`,
    })
  };

  const response = await fetch("https://api.sendinblue.com/v3/smtp/email", requestOptions);
  return response;
}