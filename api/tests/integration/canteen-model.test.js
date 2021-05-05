const { sequelize } = require('../../infrastructure/postgres-database')
const { Canteen } = require('../../infrastructure/models/canteen')
const { createCanteen, getCanteenById } = require('../../infrastructure/repositories/canteen');
const { NotFoundError } = require('../../infrastructure/errors');

const canteenPayload = {
  name: "Test canteen",
  city: "Lyon",
  sector: "school"
};

describe('Canteen repository', () => {

  beforeAll(async () => {
    await Canteen.sync({ force: true });
  });

  describe('createCanteen', () => {
    it('successfully creates one canteen given valid data', async () => {
      const createdCanteen = await createCanteen(canteenPayload);

      const canteens = await Canteen.findAll();
      expect(canteens.length).toBe(1);
      expect(createdCanteen.toJSON()).toStrictEqual(canteens[0].toJSON());
    });
  });

  describe('getCanteenById', () => {
    it('get canteen by id successfully', async () => {
      const createdCanteen = await createCanteen(canteenPayload);

      const foundCanteen = await getCanteenById(createdCanteen.id);

      expect(foundCanteen.name).toBe(canteenPayload.name);
    });

    it('throws error if canteen is not found', async () => {
      await expect(getCanteenById(6666666)).rejects.toThrow(NotFoundError);
    });
  });

  afterAll(async () => {
    await sequelize.close();
  });

});
