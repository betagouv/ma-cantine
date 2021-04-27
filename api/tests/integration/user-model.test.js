const { sequelize } = require('../../infrastructure/postgres-database');
const { Canteen } = require('../../infrastructure/models/canteen');
const { User } = require('../../infrastructure/models/user');
const { createCanteen } = require('../../infrastructure/repositories/canteen');
const { createUser, createUserWithCanteen, findUser } = require('../../infrastructure/repositories/user');

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

  beforeEach(async () => {
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    // need canteen to exist to create user
    canteenId = (await createCanteen(canteenPayload)).id;
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

  it('returns existing user given duplicate user to create', async () => {
    const createdUser = await createUserWithCanteen(userPayload, canteenPayload);
    const foundUser = await createUserWithCanteen(userPayload, {
      name: "This shouldn't exist",
      city: "Atlantis",
      sector: "fake"
    });
    expect(foundUser.id).toBe(createdUser.id);
    const badCanteen = await Canteen.findOne({ where: { city: "Atlantis" } });
    expect(badCanteen).toBeNull();
  });

  it('does not create new canteen if user fails to create', async () => {
    try {
      await createUserWithCanteen({ firstName: "Incomplete" }, canteenPayload);
    } catch(e) {}
    const users = await User.findAll();
    expect(users.length).toBe(0);
    const canteens = await Canteen.findAll();
    expect(canteens.length).toBe(1); // only have the one created in beforeEach
  });

  it('finds user successfully', async () => {
    const createdUser = await createUser(userPayload, canteenId);
    const foundUser = await findUser(userPayload);
    expect(foundUser.id).toBe(createdUser.id);
    expect(foundUser.email).toBe(createdUser.email);
  });

  afterAll(async () => {
    await sequelize.close();
  });
});
