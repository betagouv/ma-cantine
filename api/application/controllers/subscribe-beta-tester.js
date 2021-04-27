const _ = require('lodash');
const { sendEmail } = require('../../domain/services/mailer');

// TODO: refactor into call to a new usecase
async function subscribeBetaTester(request, h) {
  const payload = request.payload;
  const form = payload.form;

  let measuresHtml = '';
  payload.keyMeasures.forEach(measure => {
    measuresHtml += `<p><b>${measure.shortTitle} :</b></p>`;
    measure.subMeasures.forEach(subMeasure => {
      // If move key measures to back-end, put back STATUSES[subMeasure.status] to francise
      measuresHtml += `<p>${subMeasure.shortTitle} : ${subMeasure.status || ''}</p>`
    });
  });

  // TODO: better way of generating html string (ejs.renderFile ?)
  const htmlBody = `<!DOCTYPE html> <html> <body>` +
                    `<p><b>Cantine:</b> ${_.escape(form.school)}</p>` +
                    `<p><b>Ville:</b> ${_.escape(form.city)}</p>` +
                    `<p><b>Email:</b> ${_.escape(form.email)}</p>` +
                    `<p><b>Téléphone:</b> ${_.escape(form.phone || '')}</p>` +
                    `<p><b>Message:</b></p>` +
                    `<p>${_.escape(form.message || '')}</p>` +
                    `${measuresHtml}` +
                    `</body> </html>`;

  const response = await sendEmail([{ email: process.env.SENDINBLUE_CONTACT_EMAIL }], "Nouveau Béta-testeur ma cantine", htmlBody);
  const json = await response.json();

  return h.response({ message: json.message }).code(response.status);
}

exports.subscribeBetaTester = subscribeBetaTester;