const jwt = require('jsonwebtoken');
const { completeLogin } = require('../../../domain/usecases/complete-login');
const { NotFoundError } = require('../../../infrastructure/errors');

jest.mock('../../../infrastructure/repositories/login-token');
const { getUserForLoginToken } = require('../../../infrastructure/repositories/login-token');

describe('Log in completion', () => {

  it('generates a JSON web token given a valid login token', async () => {
    const user = { email: "some@email.com" };
    getUserForLoginToken.mockReturnValue(user);
    const res = await completeLogin('somelogintoken');
    expect(jwt.decode(res.jwt).email).toBe(user.email);
  });

  it('throws an error given an invalid token', async () => {
    getUserForLoginToken.mockRejectedValue(new NotFoundError());
    await expect(async () => {
      await completeLogin('notatoken');
    }).rejects.toThrow(NotFoundError);
  });

});
