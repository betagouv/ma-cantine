const jwt = require('jsonwebtoken');
const { initiateMagicLinkLogin, generateJWTokenForUser } = require('../../application/login');

jest.mock('node-fetch');
const fetch = require('node-fetch');

jest.mock('../../infrastructure/repositories/login-token', () => ({
  saveTokenForUser: jest.fn(),
  getUserForLoginToken: jest.fn()
}));
const { saveTokenForUser, getUserForLoginToken } = require('../../infrastructure/repositories/login-token');

jest.mock('../../infrastructure/repositories/user', () => ({
  findUser: jest.fn()
}));
const { findUser } = require('../../infrastructure/repositories/user');

jest.mock('../../application/sign-up', () => ({
  sendSignUpLink: jest.fn()
}));
const { sendSignUpLink } = require('../../application/sign-up');

const user = {
  email: "test@email.com"
};

describe('Log in', () => {

  beforeAll(() => {
    saveTokenForUser.mockResolvedValue(0);
    fetch.mockReturnValue({
      status: 201
    });
  });

  it('generates, saves, and emails temp token given known email', async () => {
    findUser.mockReturnValue(user);
    await initiateMagicLinkLogin(user.email);
    expect(saveTokenForUser).toHaveBeenCalledTimes(1);
    const token = saveTokenForUser.mock.calls[0][1]; // token is second argument
    expect(token).toBeDefined();

    // mock fetch call
    const responseBodyJSON = { message: "test" };
    fetch.mockReturnValue({
      status: 201,
      json() {
        return Promise.resolve(responseBodyJSON);
      }
    });

    expect(fetch).toHaveBeenCalledTimes(1);
    const emailEndpoint = fetch.mock.calls[0][0];
    expect(emailEndpoint).toBe("https://api.sendinblue.com/v3/smtp/email");
    const requestBody = JSON.parse(fetch.mock.calls[0][1].body);
    expect(requestBody.to).toStrictEqual([{ email: user.email }]);
    expect(requestBody.htmlContent).toMatch('?token='+encodeURIComponent(token));
  });

  it('does not send login link given unknown email', async () => {
    findUser.mockResolvedValue(null);
    await initiateMagicLinkLogin('unknown@test.com');
    expect(saveTokenForUser).not.toHaveBeenCalled();
    expect(sendSignUpLink).toHaveBeenCalledTimes(1);
  });

  it('generates unique tokens', async () => {
    findUser.mockReturnValue(user);
    await initiateMagicLinkLogin(user.email);
    await initiateMagicLinkLogin(user.email);
    const token1 = saveTokenForUser.mock.calls[0][1];
    const token2 = saveTokenForUser.mock.calls[1][1];
    expect(token1).not.toBe(token2);
  });

  it('generates a JSON web token given a valid login token', async () => {
    findUser.mockReturnValue(user);
    await initiateMagicLinkLogin(user.email);
    const loginToken = saveTokenForUser.mock.calls[0][1];
    getUserForLoginToken.mockReturnValue(user);
    const token = await generateJWTokenForUser(loginToken);
    expect(jwt.decode(token).email).toBe(user.email);
  });

  afterEach(() => {
    saveTokenForUser.mockClear();
    findUser.mockClear();
    fetch.mockClear();
  });

  // TODO: check appropriate rate limiting on email sending
});
