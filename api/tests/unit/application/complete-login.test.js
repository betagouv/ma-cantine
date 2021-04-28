const { handler } = require("../../../application/routes/complete-login");
const { NotFoundError } = require("../../../infrastructure/errors");
const { hFake } = require('../../test-helper');

jest.mock("../../../domain/usecases/complete-login");
const { completeLogin } = require("../../../domain/usecases/complete-login");

describe('Complete login handler', () => {
  it('returns login completion response given known login token', async () => {
    const completeLoginResponse = { jwt: "xxx.yyy.zzz" };
    completeLogin.mockReturnValue(completeLoginResponse);
    const res = await handler({ query: { token: 'arealtoken' }}, hFake);
    expect(res.statusCode).toBe(200);
    expect(res.result).toStrictEqual(completeLoginResponse);
    expect(completeLogin).toHaveBeenCalledWith('arealtoken');
  });

  it('returns a 400 given invalid token', async () => {
    completeLogin.mockRejectedValue(new NotFoundError());
    const res = await handler({ query: { token: 'notatoken' }}, hFake);
    expect(res.statusCode).toBe(400);
  });
});
