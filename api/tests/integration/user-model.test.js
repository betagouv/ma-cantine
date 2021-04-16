const { sequelize } = require('../../infrastructure/postgres-database');
const { Canteen } = require('../../infrastructure/models/canteen');
const { User } = require('../../infrastructure/models/user');
const { createCanteen } = require('../../infrastructure/repositories/canteen');
const { createUser, createUserWithCanteen } = require('../../infrastructure/repositories/user');

const canteenPayload = {
  name: "Test canteen",
  department: "Bouches-du-Rhône",
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
    let users = await User.findAll();
    expect(users.length).toBe(0); // make sure anything in db was added in this test

    await createUser(userPayload, canteenId);

    users = await User.findAll();
    expect(users.length).toBe(1);
    const user = users[0];
    expect(user.firstName).toBe(userPayload.firstName);
    expect(user.lastName).toBe(userPayload.lastName);
    expect(user.email).toBe(userPayload.email);
    expect(user.id).toBe(1);
    expect(user.canteenId).toBe(canteenId);
  });

  it('successfully increments user ids', async () => {
    const user1 = await createUser(userPayload, canteenId);
    userPayload.email = "other@other.com";
    const user2 = await createUser(userPayload, canteenId);
    expect(user1.id).toBe(user2.id - 1);
  });

  it('fails to create a user given invalid email', async () => {
    const badEmail = {
      firstName: userPayload.firstName,
      lastName: userPayload.lastName,
      email: "badEmail@incomplete"
    };
    await expect(createUser(badEmail)).rejects.toThrow();
    const users = await User.findAll();
    expect(users.length).toBe(0);
  });

  it('fails to create a user given duplicate email', async () => {
    await createUser(userPayload, canteenId);
    await expect(createUser({
      email: userPayload.email,
      firstName: "Other",
      lastName: "Other",
    }, canteenId)).rejects.toThrow();
    const users = await User.findAll();
    expect(users.length).toBe(1);
  });

  it('successfully creates user and canteen in database given valid data', async () => {
    const request = {
      payload: {
        user: userPayload,
        canteen: canteenPayload
      }
    };
    await createUserWithCanteen(request);

    const canteens = await Canteen.findAll();
    const users = await User.findAll();
    // use second canteen because a canteen was created in tests setup
    expect(users[0].canteenId).toBe(canteens[1].id);
  });

  afterAll(async () => {
    await sequelize.close();
  });
});
