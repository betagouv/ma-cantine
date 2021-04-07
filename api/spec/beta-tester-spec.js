const { init } = require('../server');
const FetchWrapper = require('../fetch');

describe("Beta-tester creation endpoint /subscribe-beta-tester", () => {
  let server;

  beforeEach(async () => {
    server = await init();

    spyOn(FetchWrapper, 'fetch').and.returnValue({
      status: 201,
      json: async () => { return {}; }
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
    expect(FetchWrapper.fetch).toHaveBeenCalledTimes(1);
  });

  // fails as expected with missing environment variables (multiple tests?) - but this is testing sendinblue?
  // fails without form or keyMeasures in payload
  // server registration
});
