const { Canteen } = require('../../infrastructure/models/canteen');
const { LoginToken } = require('../../infrastructure/models/login-token');
const { User } = require('../../infrastructure/models/user');
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { init } = require('../../server');

jest.mock('../../controllers/login', () => ({
  initiateMagicLinkLogin: jest.fn(),
  generateJWTokenForUser: jest.fn()
}));
const { initiateMagicLinkLogin, generateJWTokenForUser } = require('../../controllers/login');
const { sequelize } = require('../../infrastructure/postgres-database');

const canteenPayload = {
  name: "Test canteen",
  city: "Lyon",
  sector: "school"
};

const userPayload = {
  email: "test@example.com",
  firstName: "Camille",
  lastName: "Dupont",
};

describe('Login process', () => {
  let server;

  beforeAll(async () => {
    server = await init();
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    await LoginToken.sync({ force: true });
    await createUserWithCanteen(userPayload, canteenPayload);
    userPayload.id = 1;
  });

  it('sends login link when POST valid email to /login', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/login",
      payload: {
        email: userPayload.email
      }
    });
    expect(res.statusCode).toBe(200);
    expect(initiateMagicLinkLogin).toHaveBeenCalledTimes(1);
    expect(initiateMagicLinkLogin).toHaveBeenCalledWith(userPayload.email);
  });

  it('does not leak information given invalid email POSTed to /login', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/login",
      payload: {
        email: userPayload.email
      }
    });
    expect(res.statusCode).toBe(200);
    expect(initiateMagicLinkLogin).toHaveBeenCalledTimes(1);
    expect(initiateMagicLinkLogin).toHaveBeenCalledWith(userPayload.email);
  });

  it('successfully returns a JSON web token with GET /complete-login', async () => {
    const token = 'test';
    const jwt = 'xxxx.yyyy.zzzz';
    generateJWTokenForUser.mockReturnValue(jwt);
    const res = await server.inject({
      method: "GET",
      url: "/complete-login?token="+token,
    });
    expect(res.statusCode).toBe(200);
    expect(generateJWTokenForUser).toHaveBeenCalledWith(token);
    expect(res.result.jwt).toBe(jwt);
    // TODO: is there a test I should be doing for jwt server config?
  });

  it('returns a 404 given invalid token to /complete-login', async () => {
    generateJWTokenForUser.mockReturnValue(undefined);
    const res = await server.inject({
      method: "GET",
      url: "/complete-login?token=notatoken",
    });
    expect(res.statusCode).toBe(400);
    expect(res.result).toBeNull();
  });

  afterEach(async() => {
    initiateMagicLinkLogin.mockClear();
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
