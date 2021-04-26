const { Canteen } = require('../../infrastructure/models/canteen');
const { LoginToken } = require('../../infrastructure/models/login-token');
const { User } = require('../../infrastructure/models/user');
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { init } = require('../../server');
const { sequelize } = require('../../infrastructure/postgres-database');

jest.mock('../../domain/services/initiate-login', () => ({
  initiateMagicLinkLogin: jest.fn()
}));
const { initiateMagicLinkLogin } = require('../../domain/services/initiate-login');

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

  it('returns 400 given no email at /login', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/login",
      payload: {
        email: ''
      }
    });
    expect(res.statusCode).toBe(400);
  });

  afterEach(async() => {
    initiateMagicLinkLogin.mockClear();
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
