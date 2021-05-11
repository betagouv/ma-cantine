require('dotenv').config();
const { generateJwtForUser, sendLoginLink, sendSignUpLink } = require("../../../domain/services/authentication");

jest.mock('@hapi/jwt');
const Jwt = require('@hapi/jwt');

jest.mock('crypto', () => ({
  randomBytes: jest.fn(() => ({ toString: () => "secret Token" }))
}));
const crypto = require('crypto');

jest.mock('../../../domain/services/mailer');
const { sendTransactionalEmail } = require('../../../domain/services/mailer');

jest.mock('../../../infrastructure/repositories/login-token');
const { saveLoginTokenForUser } = require('../../../infrastructure/repositories/login-token');

describe('Authentication service', () => {
  it('generates and saves a login token before sending an email with that token', async () => {
    process.env.SENDINBLUE_TEMPLATE_LOGIN = 60;

    await sendLoginLink({ email: "test@example.com" }, "https://example.com?token=");

    expect(crypto.randomBytes).toHaveBeenCalledWith(200);
    expect(saveLoginTokenForUser).toHaveBeenCalledTimes(1);
    expect(saveLoginTokenForUser).toHaveBeenCalledWith({ email: "test@example.com" }, "secret Token")

    expect(sendTransactionalEmail).toHaveBeenCalledWith([{ email:"test@example.com" }], 60, {
      LOGIN_LINK: 'https://example.com?token=secret%20Token'
    });
  });

  it('sends a sign up email', async () => {
    process.env.SENDINBLUE_TEMPLATE_SIGN_UP = 7;
    await sendSignUpLink('unknown@test.com');
    expect(sendTransactionalEmail).toHaveBeenCalledWith([{ email:"unknown@test.com" }], 7);
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