const { init } = require("../../server");
const { Canteen } = require("../../infrastructure/models/canteen");
const { User } = require("../../infrastructure/models/user");
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { generateJwtForUser } = require('../../domain/services/authentication');
const { sequelize } = require("../../infrastructure/postgres-database");

describe('Save diagnostic endpoint /save-diagnostic', () => {
  let server, user;

  beforeAll(async () => {
    server = await init();
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    user = await createUserWithCanteen({
      email: "test@example.com",
      firstName: "Camille",
      lastName: "Dupont",
    }, {
      name: "Test canteen",
      city: "Lyon",
      sector: "school"
    })
    user = user.toJSON();
  });

  it('returns user data given valid JWT', async () => {
    const res = await server.inject({
      method: 'GET',
      url: '/save-diagnostic',
      headers: {
        'Authorization': 'Bearer '+generateJwtForUser(user)
      }
    });
    expect(res.statusCode).toBe(200);
    expect(res.result.id).toStrictEqual(user.id);
  });

  it('returns 401 given JWT with unknown email', async () => {
    const res = await server.inject({
      method: 'GET',
      url: '/save-diagnostic',
      headers: {
        'Authorization': 'Bearer '+generateJwtForUser({ email: "unknown@email.com" })
      }
    });
    expect(res.statusCode).toBe(401);
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});