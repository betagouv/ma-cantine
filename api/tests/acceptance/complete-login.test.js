const { Canteen } = require('../../infrastructure/models/canteen');
const { LoginToken } = require('../../infrastructure/models/login-token');
const { User } = require('../../infrastructure/models/user');
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { init } = require('../../server');
const { sequelize } = require('../../infrastructure/postgres-database');
const { NoLoginTokenError } = require('../../domain/errors');

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

describe('Login completion', () => {
  let server, token;

  beforeAll(async () => {
    server = await init();
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    await LoginToken.sync({ force: true });
    const canteen = await Canteen.create(canteenPayload);
    userPayload.canteenId = canteen.id;
    const user = await User.create(userPayload);
    token = await LoginToken.create({
      token: "someLoginToken1234",
      userId: user.id
    });
  });

  it('successfully returns a JSON web token with GET /complete-login', async () => {
    const res = await server.inject({
      method: "GET",
      url: "/complete-login?token="+token.token,
    });
    expect(res.statusCode).toBe(200);
    expect(res.result.jwt).toBeDefined();
  });

  it('returns a 400 given invalid token to /complete-login', async () => {
    const res = await server.inject({
      method: "GET",
      url: "/complete-login?token=notatoken",
    });
    expect(res.statusCode).toBe(400);
    expect(res.result).toBeNull();
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
