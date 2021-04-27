const jwt = require('jsonwebtoken');
const { generateJWTokenForUser } = require('../../domain/usecases/complete-login');
const { NoLoginTokenError } = require('../../domain/errors');

jest.mock('../../infrastructure/repositories/login-token');
const { getUserForLoginToken } = require('../../infrastructure/repositories/login-token');

describe('Log in completion', () => {

  it('generates a JSON web token given a valid login token', async () => {
    const user = { email: "some@email.com" };
    getUserForLoginToken.mockReturnValue(user);
    const token = await generateJWTokenForUser('somelogintoken');
    expect(jwt.decode(token).email).toBe(user.email);
  });

  it('throws an error given an invalid token', async () => {
    getUserForLoginToken.mockReturnValue(undefined);
    await expect(async () => {
      await generateJWTokenForUser('notatoken');
    }).rejects.toThrow(NoLoginTokenError);
  });

});
