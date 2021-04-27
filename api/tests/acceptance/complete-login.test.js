const { Canteen } = require('../../infrastructure/models/canteen');
const { LoginToken } = require('../../infrastructure/models/login-token');
const { User } = require('../../infrastructure/models/user');
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { init } = require('../../server');
const { sequelize } = require('../../infrastructure/postgres-database');
const { NoLoginTokenError } = require('../../domain/errors');

jest.mock('../../domain/usecases/complete-login');
const { generateJWTokenForUser } = require('../../domain/usecases/complete-login');

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
  let server;

  beforeAll(async () => {
    server = await init();
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    await LoginToken.sync({ force: true });
    await createUserWithCanteen(userPayload, canteenPayload);
    userPayload.id = 1;
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
  });

  it('returns a 400 given invalid token to /complete-login', async () => {
    generateJWTokenForUser.mockRejectedValue(new NoLoginTokenError());
    const res = await server.inject({
      method: "GET",
      url: "/complete-login?token=notatoken",
    });
    expect(res.statusCode).toBe(400);
    expect(generateJWTokenForUser).toHaveBeenCalledTimes(1);
    expect(res.result).toBeNull();
  });

  it('returns a 400 given no token to /complete-login', async () => {
    const res = await server.inject({
      method: "GET",
      url: "/complete-login?",
    });
    expect(res.statusCode).toBe(400);
    expect(generateJWTokenForUser).not.toHaveBeenCalled();
  });

  afterEach(async() => {
    generateJWTokenForUser.mockClear();
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
