const { init } = require("../../server");
const { Canteen } = require("../../infrastructure/models/canteen");
const { User } = require("../../infrastructure/models/user");
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');
const { getCanteenById } = require('../../infrastructure/repositories/canteen');
const { generateJwtForUser } = require('../../domain/services/authentication');
const { sequelize } = require("../../infrastructure/postgres-database");

describe('Extend canteen infos /extend-canteen-infos', () => {
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

  it('extends the canteen infos', async () => {
    const response = await server.inject({
      method: 'POST',
      url: '/extend-canteen-infos',
      headers: {
        'Authorization': 'Bearer ' + generateJwtForUser(user)
      },
      payload: {
        name: "New canteen name",
        city: "Lyon",
        sector: "school",
        mealCount: 150,
        siret: "01234567890123",
        managementType: "direct",
      }
    });

    const updatedCanteen = await getCanteenById(user.canteenId);

    expect(response.statusCode).toBe(204);
    expect(updatedCanteen).toMatchObject({
      id: user.canteenId,
      name: "New canteen name",
      city: "Lyon",
      sector: "school",
      mealCount: 150,
      siret: "01234567890123",
      managementType: "direct",
    })
  });

  afterAll(async () => {
    await server.stop();
    await sequelize.close();
  });
});
