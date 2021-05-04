const { completeLogin } = require('../../../domain/usecases/complete-login');
const { NotFoundError } = require('../../../infrastructure/errors');

jest.mock('../../../infrastructure/repositories/login-token');
const { getUserForLoginToken } = require('../../../infrastructure/repositories/login-token');

jest.mock('../../../domain/services/authentication');
const { generateJwtForUser } = require('../../../domain/services/authentication');

describe('Log in completion', () => {

  it('generates a JSON web token given a valid login token', async () => {
    const user = { email: "some@email.com" };
    getUserForLoginToken.mockReturnValue(user);

    const testToken = 'xxx.yyy.zzz';
    generateJwtForUser.mockReturnValue(testToken);

    const res = await completeLogin('somelogintoken');
    expect(generateJwtForUser).toHaveBeenCalledWith(user);
    expect(res).toStrictEqual({ jwt: testToken });
  });

  it('throws an error given an invalid token', async () => {
    getUserForLoginToken.mockRejectedValue(new NotFoundError());
    await expect(async () => {
      await completeLogin('notatoken');
    }).rejects.toThrow(NotFoundError);
  });

});
