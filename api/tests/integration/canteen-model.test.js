const { sequelize } = require('../../infrastructure/postgres-database')
const { Canteen } = require('../../infrastructure/models/canteen')
const { createCanteen } = require('../../infrastructure/repositories/canteen');

const canteenPayload = {
  name: "Test canteen",
  city: "Lyon",
  sector: "school"
};

describe('Canteen model', () => {

  beforeAll(async () => {
    await Canteen.sync({ force: true });
  });

  it('successfully creates one canteen given valid data', async () => {
    const createdCanteen = await createCanteen(canteenPayload);

    const canteens = await Canteen.findAll();
    expect(canteens.length).toBe(1);

    const persistedCanteen = await Canteen.findByPk(createdCanteen.id);
    expect(createdCanteen.toJSON()).toStrictEqual(persistedCanteen.toJSON());
  });

  afterAll(async () => {
    await sequelize.close();
  });

});
