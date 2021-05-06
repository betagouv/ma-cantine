const { subscribeNewsletter } = require('../../../domain/usecases/subscribe-newsletter');

jest.mock('node-fetch');
const fetch = require('node-fetch');

describe("Newsletter subscription", () => {
  it('calls fetch with the expected options', async () => {
    process.env.SENDINBLUE_API_KEY = "api-key";
    process.env.SENDINBLUE_LIST_ID = "666";

    await subscribeNewsletter("test@email.com");

    expect(fetch).toHaveBeenCalledWith("https://api.sendinblue.com/v3/contacts", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': 'api-key'
      },
      body: '{"email":"test@email.com","listIds":[666],"updateEnabled":true}'
    });
  });
});
