const { Canteen } = require('../../infrastructure/models/canteen');
const { LoginToken } = require('../../infrastructure/models/login-token');
const { User } = require('../../infrastructure/models/user');
const { sequelize } = require('../../infrastructure/postgres-database');
const { saveLoginTokenForUser, getUserForLoginToken } = require('../../infrastructure/repositories/login-token');
const { createUserWithCanteen } = require('../../infrastructure/repositories/user');

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

describe('Login token model', () => {
  const tokenString = 'testtoken1234';
  let user;

  beforeAll(async () => {
    await Canteen.sync({ force: true });
    await User.sync({ force: true });
    await LoginToken.sync({ force: true });
    // need to create user and canteen because userId is foreign key in LoginToken
    user = await createUserWithCanteen(userPayload, canteenPayload);
  });

  beforeEach(async () => {
    await LoginToken.destroy({
      truncate: true
    });
  });

  it('saves token', async () => {
    await saveLoginTokenForUser(user, tokenString);
    const tokens = await LoginToken.findAll({
      where: {
        userId: user.id
      }
    });
    expect(tokens.length).toBe(1);
    const token = tokens[0];
    expect(token.userId).toBe(user.id);
    expect(token.token).toBe(tokenString);
    expect(token.expirationDate).toBeDefined(); // TODO: check < 1 hour from now ?
  });

  it('updates token for user given duplicate', async () => {
    await saveLoginTokenForUser(user, 'firsttokenstring');
    await saveLoginTokenForUser(user, tokenString);
    const tokens = await LoginToken.findAll({
      where: {
        userId: user.id
      }
    });
    expect(tokens.length).toBe(1);
    const token = tokens[0];
    expect(token.token).toBe(tokenString);
  });

  it('returns user for valid token', async () => {
    await saveLoginTokenForUser(user, tokenString);
    const tokenUser = await getUserForLoginToken(tokenString);
    expect(tokenUser.email).toBe(user.email);
  });

  it('does not return user for expired token', async () => {
    const now = new Date();
    await LoginToken.create({
      userId: user.id,
      token: tokenString,
      // TODO: is this the right way to mock the date?
      createdAt: now.setHours(now.getHours() - 2)
    });
    const tokenUser = await getUserForLoginToken(tokenString);
    expect(tokenUser).not.toBeDefined();
    const tokens = await LoginToken.findAll({
      where: {
        userId: user.id
      }
    });
    expect(tokens.length).toBe(0); // getValidToken to delete expired tokens
  });

  it('deletes login token after one access', async () => {
    await saveLoginTokenForUser(user, tokenString);
    await getUserForLoginToken(tokenString);
    const tokenUser = await getUserForLoginToken(tokenString);
    expect(tokenUser).not.toBeDefined();
  });

  it('requires a user', async () => {
    await expect(saveLoginTokenForUser({ id: null }, tokenString)).rejects.toThrow();
  });

  afterAll(async () => {
    await sequelize.close();
  });

});
