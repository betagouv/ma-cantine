const { init } = require("../../server");
const { sequelize } = require("../../infrastructure/postgres-database");

jest.mock('node-fetch');
const fetch = require('node-fetch');

describe('Sign up endpoint /sign-up', () => {
  let server;

  beforeAll(async () => {
    server = await init();
  });

  it('triggers sign up on POST with valid data', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/sign-up",
      payload: {
        user: {
          email: "test@example.com",
          firstName: "Camille",
          lastName: "Dupont",
        },
        canteen: {
          name: "Test canteen",
          city: "Lyon",
          sector: "school",
          managementType: "direct"
        },
        loginUrl: "https://example.com/login?token="
      }
    });
    expect(res.statusCode).toBe(200);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it('errors if invalid data on POST', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/sign-up",
      payload: {
        user: {},
        canteen: {},
        loginUrl: "hello"
      }
    });
    expect(res.statusCode).toBe(400);
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});