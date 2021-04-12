const { init } = require('../../server');
jest.mock('node-fetch');
const fetch = require('node-fetch');

describe("Beta-tester subscription endpoint /subscribe-beta-tester", () => {
  let server;
  let responseBodyJSON = { message: "test" };

  beforeEach(async () => {
    server = await init();

    fetch.mockReturnValue({
      status: 201,
      json() {
        return Promise.resolve(responseBodyJSON);
      }
    });
  });

  afterEach(async () => {
    await server.stop();
  });

  it("returns successful response given valid payload", async () => {
    const res = await server.inject({
      method: 'POST',
      url: '/subscribe-beta-tester',
      payload: {
        keyMeasures: [
          {
            shortTitle: "Test measure 1",
            subMeasures: [{
              shortTitle: "Test sub measure 1",
              status: "done"
            }]
          }
        ],
        form: {
          school: "Test school",
          email: "requester@test.com"
        }
      }
    });
    expect(res.statusCode).toBe(201);
    expect(res.result).toStrictEqual(responseBodyJSON);
    expect(fetch).toHaveBeenCalledTimes(1);
  });
});
