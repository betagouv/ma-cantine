const { initiateMagicLinkLogin } = require('../../domain/services/initiate-login');

jest.mock('node-fetch');
const fetch = require('node-fetch');

jest.mock('../../infrastructure/repositories/login-token', () => ({
  saveLoginTokenForUser: jest.fn()
}));
const { saveLoginTokenForUser } = require('../../infrastructure/repositories/login-token');

jest.mock('../../infrastructure/repositories/user', () => ({
  findUser: jest.fn()
}));
const { findUser } = require('../../infrastructure/repositories/user');

jest.mock('../../domain/services/send-sign-up-link', () => ({
  sendSignUpLink: jest.fn()
}));
const { sendSignUpLink } = require('../../domain/services/send-sign-up-link');

const user = {
  email: "test@email.com"
};

describe('Log in initiation', () => {

  beforeAll(() => {
    saveLoginTokenForUser.mockResolvedValue(0);
    fetch.mockReturnValue({
      status: 201
    });
  });

  it('generates, saves, and emails temp token given known email', async () => {
    findUser.mockReturnValue(user);
    await initiateMagicLinkLogin(user.email);
    expect(saveLoginTokenForUser).toHaveBeenCalledTimes(1);
    const token = saveLoginTokenForUser.mock.calls[0][1]; // token is second argument
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
    expect(saveLoginTokenForUser).not.toHaveBeenCalled();
    expect(sendSignUpLink).toHaveBeenCalledTimes(1);
  });

  it('generates unique tokens', async () => {
    findUser.mockReturnValue(user);
    await initiateMagicLinkLogin(user.email);
    await initiateMagicLinkLogin(user.email);
    const token1 = saveLoginTokenForUser.mock.calls[0][1];
    const token2 = saveLoginTokenForUser.mock.calls[1][1];
    expect(token1).not.toBe(token2);
  });

  afterEach(() => {
    saveLoginTokenForUser.mockClear();
    findUser.mockClear();
    fetch.mockClear();
  });

  // TODO: check appropriate rate limiting on email sending
});
