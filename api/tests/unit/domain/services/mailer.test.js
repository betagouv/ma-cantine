const { sendEmail, sendTransactionalEmail } = require("../../../../domain/services/mailer");

jest.mock('node-fetch');
const fetch = require('node-fetch');

describe('Mailer services', () => {
  it('sends email with HTML body when sendEmail is called', async () => {
    process.env.SENDINBLUE_API_KEY = 'top_secret';
    process.env.SENDINBLUE_SENDER_EMAIL = 'sender@email.com';
    process.env.SENDINBLUE_SENDER_NAME = 'Sender name';
    process.env.SENDINBLUE_CONTACT_EMAIL = 'contact@email.com';

    await sendEmail([{ email: 'test@email.com' }], 'A nice subject', '<body>The email</body>');

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith("https://api.sendinblue.com/v3/smtp/email", {
      method: "POST",
      headers: { "Content-Type": "application/json", "api-key": 'top_secret' },
      body: '{"sender":{"email":"sender@email.com","name":"Sender name"},"to":[{"email":"test@email.com"}],"replyTo":{"email":"contact@email.com"},"subject":"A nice subject","htmlContent":"<body>The email</body>"}'
    });
  });

  it('sends email from template when sendTransactionalEmail is called', async () => {
    process.env.SENDINBLUE_API_KEY = 'top_secret';

    await sendTransactionalEmail([{ email: 'test@email.com' }], 80, { testVariable: 'test' });

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith("https://api.sendinblue.com/v3/smtp/email", {
      method: "POST",
      headers: { "Content-Type": "application/json", "api-key": 'top_secret' },
      body: '{"to":[{"email":"test@email.com"}],"templateId":80,"params":{"testVariable":"test"}}'
    });
  });

  afterEach(() => {
    fetch.mockClear();
  });
});
