const { handler } = require('../../../application/routes/sign-up');
const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/sign-up');
const { signUp } = require('../../../domain/usecases/sign-up');

describe('Sign up handler', () => {
  it('triggers sign up', async () => {
    const res = await handler({
      payload: {
        user,
        canteen,
        loginUrl
      }
    }, hFake);
    expect(res.statusCode).toBe(200);
    expect(signUp).toHaveBeenCalledTimes(1);
    expect(signUp).toHaveBeenCalledWith(user, canteen, loginUrl);
  });
});