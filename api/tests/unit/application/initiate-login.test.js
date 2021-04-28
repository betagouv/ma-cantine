const { handler } = require('../../../application/routes/initiate-login');
const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/initiate-login');
const { initiateLogin } = require('../../../domain/usecases/initiate-login');

describe('Initiate login handler', () => {
  it('initiates login', async () => {
    const res = await handler({
      payload: {
        loginUrl: 'https://example.com/login?token=',
        email: "some@email.com"
      }
    }, hFake);
    expect(res.statusCode).toBe(200);
    expect(initiateLogin).toHaveBeenCalledTimes(1);
    expect(initiateLogin).toHaveBeenCalledWith("some@email.com", 'https://example.com/login?token=');
  });
});