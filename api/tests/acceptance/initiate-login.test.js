const { Canteen } = require('../../infrastructure/models/canteen');
const { LoginToken } = require('../../infrastructure/models/login-token');
const { User } = require('../../infrastructure/models/user');
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { init } = require('../../server');
const { sequelize } = require('../../infrastructure/postgres-database');

jest.mock('node-fetch');
const fetch = require('node-fetch');

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

const loginUrl = 'https://example.com/login?token=';

describe('Login initiation endpoint /login', () => {
  let server;

  beforeAll(async () => {
    server = await init();
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    await LoginToken.sync({ force: true });
    await createUserWithCanteen(userPayload, canteenPayload);
  });

  it('sends login link when POST valid email', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/login",
      payload: {
        loginUrl,
        email: userPayload.email
      }
    });
    expect(res.statusCode).toBe(200);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it('does not leak information given unknown email', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/login",
      payload: {
        loginUrl,
        email: "unknown@email.com"
      }
    });
    expect(res.statusCode).toBe(200);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it('returns 400 given no email', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/login",
      payload: {
        loginUrl,
        email: ''
      }
    });
    expect(res.statusCode).toBe(400);
    expect(fetch).not.toHaveBeenCalled();
  });

  it('returns 400 given no URL', async () => {
    const res = await server.inject({
      method: "POST",
      url: "/login",
      payload: {
        email: 'some@email.com'
      }
    });
    expect(res.statusCode).toBe(400);
    expect(fetch).not.toHaveBeenCalled();
  });

  afterEach(async() => {
    fetch.mockClear();
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
