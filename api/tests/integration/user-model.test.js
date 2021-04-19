const { sequelize } = require('../../database/setup')
const { User, Canteen } = require('../../database/models')
const { createUser, createCanteen, createUserAndCanteen } = require('../../application/create-user-and-canteen');

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
    await sequelize.sync({ force: true });
    await createCanteen(canteenPayload); // need canteen to exist to create user
    canteenId = (await Canteen.findAll())[0].id;
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
    expect(user.managesCanteen).toBe(canteenId);
  });

  it('successfully increments user ids', async () => {
    const user1 = await createUser(userPayload, canteenId);
    userPayload.email = "other@other.com";
    const user2 = await createUser(userPayload, canteenId);
    expect(user1.id).toBe(user2.id - 1);
  });

  it('fails to create a user given invalid data', async () => {
    await expect(createUser({})).rejects.toThrow();
    const users = await User.findAll();
    expect(users.length).toBe(0);
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

  // TODO: should this test be in a different suite?
  it('successfully creates user and canteen in database given valid data', async () => {
    const request = {
      payload: {
        user: userPayload,
        canteen: canteenPayload
      }
    };
    await createUserAndCanteen(request);

    const canteens = await Canteen.findAll();
    const users = await User.findAll();
    // use second canteen because a canteen was created in beforeEach
    expect(users[0].managesCanteen).toBe(canteens[1].id);
  });

  afterAll(async () => {
    await sequelize.drop();
    await sequelize.close();
  });
});
