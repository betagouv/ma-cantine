const { Canteen } = require('../../infrastructure/models/canteen');
const { LoginToken } = require('../../infrastructure/models/login-token');
const { User } = require('../../infrastructure/models/user');
const { init } = require('../../server');
const { sequelize } = require('../../infrastructure/postgres-database');
const { Diagnostic } = require('../../infrastructure/models/diagnostic');

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

describe('Login completion endpoint /complete-login', () => {
  let server, user;

  beforeAll(async () => {
    server = await init();
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    await LoginToken.sync({ force: true });
    await Diagnostic.sync({ force: true });
    const canteen = await Canteen.create(canteenPayload);
    userPayload.canteenId = canteen.id;
    user = await User.create(userPayload);
  });

  it('successfully returns a JSON web token with POST', async () => {
    await LoginToken.create({
      token: "someLoginToken1234",
      userId: user.id
    });
    const res = await server.inject({
      method: "POST",
      url: "/complete-login",
      payload: {
        token: 'someLoginToken1234'
      }
    });
    expect(res.statusCode).toBe(200);
    expect(res.result.jwt).toBeDefined();
  });

  it('successfully returns a JSON web token and saves diagnostic data with POST', async () => {
    await LoginToken.create({
      token: "someLoginToken1234",
      userId: user.id
    });
    const res = await server.inject({
      method: "POST",
      url: "/complete-login",
      payload: {
        token: 'someLoginToken1234',
        diagnostics: [{
          year: 2019,
          valueBio: 50
        }]
      }
    });
    expect(res.statusCode).toBe(200);
    expect(res.result.jwt).toBeDefined();
    const persistedDiagnostics = await Diagnostic.findAll();
    expect(persistedDiagnostics.length).toBe(1);
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
