const { sequelize } = require('../../infrastructure/postgres-database');
const { Canteen } = require('../../infrastructure/models/canteen');
const { User } = require('../../infrastructure/models/user');
const { createCanteen } = require('../../infrastructure/repositories/canteen');
const { createUser, createUserWithCanteen, DuplicateUserError } = require('../../infrastructure/repositories/user');

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

describe('User model', () => {
  let canteenId;

  beforeAll(async () => {
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    // need canteen to exist to create user
    canteenId = (await createCanteen(canteenPayload)).id;
  });

  beforeEach(async () => {
    await User.destroy({
      truncate: true
    });
  });

  it('successfully creates user given valid data', async () => {
    const createdUser = await createUser(userPayload, canteenId);

    const users = await User.findAll();
    expect(users.length).toBe(1);

    const persistedUser = await User.findByPk(createdUser.id);
    expect(createdUser.toJSON()).toStrictEqual(persistedUser.toJSON());
    expect(createdUser.canteenId).toBe(canteenId);
  });

  it('successfully creates user and canteen in database given valid data', async () => {
    await createUserWithCanteen(userPayload, canteenPayload);

    const canteens = await Canteen.findAll();
    const users = await User.findAll();
    // use second canteen because a canteen was created in tests setup
    expect(users[0].canteenId).toBe(canteens[1].id);
  });

  it('throws user exists error given duplicate user to create', async () => {
    await createUserWithCanteen(userPayload, canteenPayload);
    await expect(async () => {
      await createUserWithCanteen(userPayload, canteenPayload);
    }).rejects.toThrow(DuplicateUserError);
  });

  afterAll(async () => {
    await sequelize.close();
  });
});
