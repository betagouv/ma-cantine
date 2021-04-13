const { sequelize } = require('../../database/setup')
const { Canteen } = require('../../database/models')
const { createCanteen } = require('../../application/create-user-and-canteen');

const canteenPayload = {
  name: "Test canteen",
  city: "Lyon",
  sector: "school"
};

describe('Canteen model', () => {

  beforeEach(async () => {
    await sequelize.sync({ force: true });
  });

  it('successfully creates canteen given valid data', async () => {
    let canteens = await Canteen.findAll();
    expect(canteens.length).toBe(0); // make sure anything in db was added in this test

    await createCanteen(canteenPayload);

    canteens = await Canteen.findAll();
    expect(canteens.length).toBe(1);
    const canteen = canteens[0];
    expect(canteen.name).toBe(canteenPayload.name);
    expect(canteen.city).toBe(canteenPayload.city);
    expect(canteen.sector).toBe(canteenPayload.sector);
    expect(canteen.id).toBe(1);
  });

  it('fails to create a canteen given invalid data', async () => {
    await expect(createCanteen({})).rejects.toThrow();
    const canteens = await Canteen.findAll();
    expect(canteens.length).toBe(0);
  });

  afterAll(async () => {
    await sequelize.drop();
    await sequelize.close();
  });

});
