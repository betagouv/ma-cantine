const { handler } = require("../../../application/routes/complete-login");
const { NotFoundError } = require("../../../infrastructure/errors");

// mock dependencies
jest.mock("../../../domain/usecases/complete-login");
const { completeLogin } = require("../../../domain/usecases/complete-login");

describe('Complete login handler', () => {
  const hFake = {
    response() { return this; },
    code(code) {
      this.statusCode = code;
      return this;
    }
  };

  it('returns a 400 given invalid token', async () => {
    completeLogin.mockRejectedValue(new NotFoundError());
    const res = await handler({ query: { token: 'notatoken' }}, hFake);
    expect(res.statusCode).toBe(400);
    expect(completeLogin).toHaveBeenCalledWith('notatoken');
  });
});
