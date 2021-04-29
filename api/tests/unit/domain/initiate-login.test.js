const { initiateLogin } = require('../../../domain/usecases/initiate-login');

jest.mock('node-fetch');
const fetch = require('node-fetch');

jest.mock('../../../infrastructure/repositories/login-token');
const { saveLoginTokenForUser } = require('../../../infrastructure/repositories/login-token');

jest.mock('../../../infrastructure/repositories/user');
const { getUserByEmail } = require('../../../infrastructure/repositories/user');
const { NotFoundError } = require('../../../infrastructure/errors');

const user = {
  email: "test@email.com"
};

const URL_PREFIX = 'https://example.com/login?token=';

describe('Log in initiation', () => {

  beforeAll(() => {
    saveLoginTokenForUser.mockResolvedValue(0);
    fetch.mockReturnValue({
      status: 201
    });
  });

  it('generates, saves, and emails temp token given known email', async () => {
    getUserByEmail.mockReturnValue(user);
    await initiateLogin(user.email, URL_PREFIX);
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
    const requestBody = JSON.parse(fetch.mock.calls[0][1].body);
    expect(requestBody.to).toStrictEqual([{ email: user.email }]);
    expect(requestBody.htmlContent).toMatch(URL_PREFIX+encodeURIComponent(token));
  });

  it('sends a sign up, not login, link given unknown email', async () => {
    getUserByEmail.mockRejectedValue(new NotFoundError());
    await initiateLogin('unknown@test.com', URL_PREFIX);
    expect(saveLoginTokenForUser).not.toHaveBeenCalled();

    // mock fetch call
    const responseBodyJSON = { message: "test" };
    fetch.mockReturnValue({
      status: 201,
      json() {
        return Promise.resolve(responseBodyJSON);
      }
    });

    expect(fetch).toHaveBeenCalledTimes(1);
    const requestBody = JSON.parse(fetch.mock.calls[0][1].body);
    expect(requestBody.to).toStrictEqual([{ email: 'unknown@test.com' }]);
  });

  it('generates unique tokens', async () => {
    getUserByEmail.mockReturnValue(user);
    await initiateLogin(user.email, URL_PREFIX);
    await initiateLogin(user.email, URL_PREFIX);
    const token1 = saveLoginTokenForUser.mock.calls[0][1];
    const token2 = saveLoginTokenForUser.mock.calls[1][1];
    expect(token1).not.toBe(token2);
  });

  afterEach(() => {
    saveLoginTokenForUser.mockClear();
    getUserByEmail.mockClear();
    fetch.mockClear();
  });

  // TODO: check appropriate rate limiting on email sending
});
