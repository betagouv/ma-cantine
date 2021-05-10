const { init } = require("../../server");
const { Canteen } = require("../../infrastructure/models/canteen");
const { User } = require("../../infrastructure/models/user");
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { getCanteenById } = require('../../infrastructure/repositories/canteen');
const { generateJwtForUser } = require('../../domain/services/authentication');
const { sequelize } = require("../../infrastructure/postgres-database");

describe('Complete publication /complete-publication', () => {
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
      sector: "school",
    })
  });

  it('completes the publication', async () => {
    const response = await server.inject({
      method: 'POST',
      url: '/complete-publication',
      headers: {
        'Authorization': 'Bearer ' + generateJwtForUser(user)
      },
      payload: {
        makeDataPublic: true
      }
    });

    const updatedCanteen = await getCanteenById(user.canteenId);

    expect(response.statusCode).toBe(204);
    expect(updatedCanteen).toMatchObject({
      id: user.canteenId,
      hasPublished: true,
      dataIsPublic: true,
    })
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
