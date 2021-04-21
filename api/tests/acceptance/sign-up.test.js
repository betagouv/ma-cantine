const { init } = require("../../server");

jest.mock("../../infrastructure/repositories/user", () => ({
  createUserWithCanteen: jest.fn()
}));
const { createUserWithCanteen, createUser } = require("../../infrastructure/repositories/user");

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

describe('Sign up endpoint /sign-up', () => {
  let server;

  beforeAll(async () => {
    server = await init();
  });

  it('triggers user creation on POST with valid data', async () => {
    createUserWithCanteen.mockReturnValue(user);
    const res = await server.inject({
      method: "POST",
      url: "/sign-up",
      payload: {
        user,
        canteen
      }
    });
    expect(res.statusCode).toBe(201);
    expect(createUserWithCanteen).toHaveBeenCalledTimes(1);
    expect(createUserWithCanteen).toHaveBeenCalledWith(user, canteen);
  });

  // TODO:
  // it('triggers login link on POST to /sign-up if duplicate email', async() => {
  //   const res = await server.inject({

  //   })
  // })

  it('errors if invalid data on POST', async () => {
    createUserWithCanteen.mockReturnValue();
    const res = await server.inject({
      method: "POST",
      url: "/sign-up",
      payload: {
        user: {},
        canteen: {}
      }
    });
    expect(res.statusCode).toBe(400);
  });

  afterAll(async () => {
    await server.stop();
  });
});