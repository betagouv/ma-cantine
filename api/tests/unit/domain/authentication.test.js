require('dotenv').config();
const { generateJwtForUser, sendLoginLink, sendSignUpLink } = require("../../../domain/services/authentication");

jest.mock('@hapi/jwt');
const Jwt = require('@hapi/jwt');

jest.mock('../../../domain/services/mailer');
const { sendTransactionalEmail } = require('../../../domain/services/mailer');

jest.mock('../../../infrastructure/repositories/login-token');
const { saveLoginTokenForUser } = require('../../../infrastructure/repositories/login-token');

describe('Authentication service', () => {
  it('generates and saves a login token before sending an email with that token', async () => {
    process.env.SENDINBLUE_TEMPLATE_LOGIN = 60;

    await sendLoginLink({ email: "test@example.com" }, "https://example.com?token=");

    expect(saveLoginTokenForUser).toHaveBeenCalledTimes(1);
    expect(saveLoginTokenForUser.mock.calls[0][0]).toStrictEqual({ email: "test@example.com" });
    const token = saveLoginTokenForUser.mock.calls[0][1]; // token is second argument
    expect(token).toBeDefined();

    expect(sendTransactionalEmail).toHaveBeenCalledWith([{ email:"test@example.com" }], 60, {
      LINK: 'https://example.com?token='+encodeURIComponent(token)
    });
  });

  it('sends a sign up email', async () => {
    process.env.SENDINBLUE_TEMPLATE_SIGN_UP = 7;
    await sendSignUpLink('unknown@test.com');
    expect(sendTransactionalEmail).toHaveBeenCalledWith([{ email:"unknown@test.com" }], 7);
  });

  it('generates unique login tokens', async () => {
    await sendLoginLink("user@email.com", "");
    await sendLoginLink("user@email.com", "");
    const token1 = saveLoginTokenForUser.mock.calls[0][1];
    const token2 = saveLoginTokenForUser.mock.calls[1][1];
    expect(token1).not.toBe(token2);
  });

  it('uses user email and secret key to generate JWT', () => {
    process.env.JWT_SECRET_KEY = 'topSecretKey';
    const mockedToken = "xxx.yyy.zzz";
    Jwt.token.generate.mockReturnValue(mockedToken);
    const jwt = generateJwtForUser({
      email: "example@test.com"
    });
    expect(Jwt.token.generate).toHaveBeenCalledWith({ email: "example@test.com" }, 'topSecretKey');
    expect(jwt).toBe(mockedToken);
  });

  // TODO: check appropriate rate limiting on email sending

  afterEach(() => {
    saveLoginTokenForUser.mockClear();
    sendTransactionalEmail.mockClear();
  });
});