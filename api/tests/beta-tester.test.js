const { init } = require('../server');
jest.mock('node-fetch');
const fetch = require('node-fetch');
const { Response, Headers } = jest.requireActual('node-fetch');

describe("Beta-tester creation endpoint /subscribe-beta-tester", () => {
  let server;
  let responseBodyJSON = { message: "test" };

  beforeEach(async () => {
    server = await init();

    responseInit = {
      status: 201,
      headers: new Headers({
        'Content-Type': 'application/json'
      })
    };
    fetch.mockReturnValue(
      Promise.resolve(new Response(JSON.stringify(responseBodyJSON), responseInit))
    );
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
          },
          {
            shortTitle: "Test measure 2",
            subMeasures: [{
              shortTitle: "Test sub measure 2",
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

  // TODO: fails as expected with missing environment variables
  // TODO: fails without form or keyMeasures in payload
});
