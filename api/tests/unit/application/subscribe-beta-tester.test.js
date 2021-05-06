const { subscribeBetaTesterHandler } = require('../../../application/routes/subscribe-beta-tester');
const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/subscribe-beta-tester');
const { subscribeBetaTester } = require('../../../domain/usecases/subscribe-beta-tester');

describe('Subscribe Beta Tester handler', () => {
  it('triggers subscribe-beta-tester', async () => {
    subscribeBetaTester.mockReturnValue({
      status: 201,
      json() {
        return Promise.resolve({ message: "test" });
      }
    });

    const response = await subscribeBetaTesterHandler({
      payload: { email: "test@email.com" }
    }, hFake);

    expect(response.statusCode).toBe(201);
    expect(response.result).toStrictEqual({ message: "test" });
    expect(subscribeBetaTester).toHaveBeenCalledWith({ email: "test@email.com" });
  });
});
