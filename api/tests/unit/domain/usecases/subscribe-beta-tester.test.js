const { subscribeBetaTester } = require('../../../../domain/usecases/subscribe-beta-tester');

jest.mock('../../../../domain/services/mailer');
const { sendEmail } = require('../../../../domain/services/mailer');

describe("Beta Tester subscription", () => {
  it('calls sendEmail with the expected parameters', async () => {
    process.env.SENDINBLUE_CONTACT_EMAIL = "contact@mail.com";

    await subscribeBetaTester({
      email: "test@email.com",
      city: "Toulouse",
      school: "Poudlard",
      phone: "555-808",
      message: "Count me in",
    });

    expect(sendEmail).toHaveBeenCalledWith(
      [{ email: "contact@mail.com" }],
      "Nouveau Béta-testeur ma cantine",
      "<!DOCTYPE html> <html> <body><p><b>Cantine:</b> Poudlard</p><p><b>Ville:</b> Toulouse</p><p><b>Email:</b> test@email.com</p><p><b>Téléphone:</b> 555-808</p><p><b>Message:</b></p><p>Count me in</p></body> </html>"
    );
  });
});
