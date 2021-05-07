const { initiateLogin } = require('../../../domain/usecases/initiate-login');

jest.mock('../../../infrastructure/repositories/login-token');
const { saveLoginTokenForUser } = require('../../../infrastructure/repositories/login-token');

jest.mock('../../../infrastructure/repositories/user');
const { getUserByEmail } = require('../../../infrastructure/repositories/user');
const { NotFoundError } = require('../../../infrastructure/errors');

jest.mock('../../../domain/services/mailer');
const { sendTransactionalEmail } = require('../../../domain/services/mailer');

const user = {
  email: "test@email.com"
};

const URL_PREFIX = 'https://example.com/login?token=';

describe('Log in initiation', () => {

  beforeAll(() => {
    saveLoginTokenForUser.mockResolvedValue(0);
  });

  // TODO: isolate dependencies properly
  it('generates, saves, and emails temp token given known email', async () => {
    process.env.SENDINBLUE_TEMPLATE_LOGIN = 60;
    getUserByEmail.mockReturnValue(user);

    await initiateLogin(user.email, URL_PREFIX);

    expect(saveLoginTokenForUser).toHaveBeenCalledTimes(1);
    const token = saveLoginTokenForUser.mock.calls[0][1]; // token is second argument
    expect(token).toBeDefined();

    expect(sendTransactionalEmail).toHaveBeenCalledWith([{ email:"test@email.com" }], 60, { LINK: 'https://example.com/login?token='+encodeURIComponent(token) });
  });

  it('sends a sign up, not login, link given unknown email', async () => {
    process.env.SENDINBLUE_TEMPLATE_SIGN_UP = 7;
    getUserByEmail.mockRejectedValue(new NotFoundError());
    await initiateLogin('unknown@test.com', URL_PREFIX);
    expect(saveLoginTokenForUser).not.toHaveBeenCalled();

    expect(sendTransactionalEmail).toHaveBeenCalledWith([{ email:"unknown@test.com" }], 7);
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
    sendTransactionalEmail.mockClear();
  });

  // TODO: check appropriate rate limiting on email sending
});
