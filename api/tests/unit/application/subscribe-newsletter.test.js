const { subscribeNewsletterHandler } = require('../../../application/routes/subscribe-newsletter');
const { hFake } = require('../../test-helper');

jest.mock('../../../domain/usecases/subscribe-newsletter');
const { subscribeNewsletter } = require('../../../domain/usecases/subscribe-newsletter');

describe('Subscribe Newsletter handler', () => {
  it('triggers subscribe-newsletter', async () => {
    subscribeNewsletter.mockReturnValue({
      status: 201,
      json() {
        return Promise.resolve({ message: "test" });
      }
    });

    const response = await subscribeNewsletterHandler({
      payload: { email: "test@email.com" }
    }, hFake);

    expect(response.statusCode).toBe(201);
    expect(response.result).toStrictEqual({ message: "test" });
    expect(subscribeNewsletter).toHaveBeenCalledWith("test@email.com");
  });
});
