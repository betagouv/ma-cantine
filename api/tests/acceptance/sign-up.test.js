const { init } = require("../../server");

jest.mock("../../domain/usecases/sign-up");
const { signUp } = require("../../domain/usecases/sign-up");

const canteen = {
  name: "Test canteen",
  city: "Lyon",
  sector: "school"
};

const user = {
  email: "test@example.com",
  firstName: "Camille",
  lastName: "Dupont",
};

const loginUrl = "https://example.com/login?token=";

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
        user,
        canteen,
        loginUrl
      }
    });
    expect(res.statusCode).toBe(200);
    expect(signUp).toHaveBeenCalledTimes(1);
    expect(signUp).toHaveBeenCalledWith(user, canteen, loginUrl);
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
  });
});