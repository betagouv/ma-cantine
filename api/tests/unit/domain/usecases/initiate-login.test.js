const { initiateLogin } = require('../../../../domain/usecases/initiate-login');

jest.mock('../../../../infrastructure/repositories/user');
const { getUserByEmail } = require('../../../../infrastructure/repositories/user');
const { NotFoundError } = require('../../../../infrastructure/errors');

jest.mock('../../../../domain/services/authentication');
const { sendLoginLink, sendSignUpLink } = require('../../../../domain/services/authentication');

describe('Log in initiation', () => {
  it('generates, saves, and emails temp token given known email', async () => {
    getUserByEmail.mockReturnValue({ email: "test@example.com" });

    await initiateLogin("test@example.com", "https://example.com/");

    expect(sendLoginLink).toHaveBeenCalledTimes(1);
    expect(sendLoginLink).toHaveBeenCalledWith({ email: "test@example.com" }, "https://example.com/");
  });

  it('sends a sign up, not login, link given unknown email', async () => {
    getUserByEmail.mockRejectedValue(new NotFoundError());

    await initiateLogin("test@example.com", "https://example.com/");

    expect(sendSignUpLink).toHaveBeenCalledTimes(1);
    expect(sendSignUpLink).toHaveBeenCalledWith("test@example.com");
    expect(sendLoginLink).not.toHaveBeenCalled();
  });

  it('passes up unknown error', async () => {
    getUserByEmail.mockRejectedValue(new Error());
    await expect(initiateLogin('email', 'url')).rejects.toThrow(Error);
  });

  afterEach(() => {
    getUserByEmail.mockClear();
    sendLoginLink.mockClear();
    sendSignUpLink.mockClear();
  });
});
