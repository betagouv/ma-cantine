const { sequelize } = require('../../infrastructure/postgres-database')
const { Canteen } = require('../../infrastructure/models/canteen')
const { createCanteen } = require('../../infrastructure/repositories/canteen');

const canteenPayload = {
  name: "Test canteen",
  department: "Bouches-du-Rhône",
  sector: "school"
};

describe('Canteen model', () => {

  beforeAll(async () => {
    await Canteen.sync({ force: true });
  });

  it('successfully creates canteen given valid data', async () => {
    let canteens = await Canteen.findAll();
    expect(canteens.length).toBe(0); // make sure anything in db was added in this test

    await createCanteen(canteenPayload);

    canteens = await Canteen.findAll();
    expect(canteens.length).toBe(1);
    const canteen = canteens[0];
    expect(canteen.name).toBe(canteenPayload.name);
    expect(canteen.department).toBe(canteenPayload.department);
    expect(canteen.sector).toBe(canteenPayload.sector);
    expect(canteen.id).toBe(1);
  });

  afterAll(async () => {
    await sequelize.close();
  });

});
