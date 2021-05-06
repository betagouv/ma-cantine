const { init } = require('../../server');

jest.mock('node-fetch');
const fetch = require('node-fetch');

describe("Beta-tester subscription endpoint /subscribe-beta-tester", () => {
  let server;

  beforeAll(async () => {
    server = await init();

    fetch.mockReturnValue({
      status: 201,
      json() {
        return Promise.resolve({ message: "test" });
      }
    });
  });

  it("returns successful response given valid payload", async () => {
    const response = await server.inject({
      method: 'POST',
      url: '/subscribe-beta-tester',
      payload: {
        school: "Test school",
        email: "requester@test.com"
      }
    });

    expect(response.statusCode).toBe(201);
    expect(response.result).toStrictEqual({ message: "test" });
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  afterAll(async () => {
    await server.stop();
  });
});
