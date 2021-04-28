const { NotFoundError } = require('../../infrastructure/errors');
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
    user.id = 1;
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
    expect(token.expirationDate).toBeDefined();
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

  it('throws error given expired token and deletes it from database', async () => {
    const now = new Date();
    await LoginToken.create({
      userId: user.id,
      token: tokenString,
      createdAt: now.setHours(now.getHours() - 2)
    });
    await expect(getUserForLoginToken(tokenString)).rejects.toThrow(NotFoundError);
    await expect(getUserForLoginToken(tokenString)).rejects.toThrow(/testtoken1234/);
    const tokens = await LoginToken.findAll({
      where: {
        userId: user.id
      }
    });
    expect(tokens.length).toBe(0);
  });

  it('deletes login token after one access', async () => {
    await saveLoginTokenForUser(user, tokenString);
    await getUserForLoginToken(tokenString);
    await expect(getUserForLoginToken(tokenString)).rejects.toThrow(NotFoundError);
    await expect(getUserForLoginToken(tokenString)).rejects.toThrow(/testtoken1234/);
  });

  it('requires a user', async () => {
    await expect(saveLoginTokenForUser({ id: null }, tokenString)).rejects.toThrow();
  });

  afterAll(async () => {
    await sequelize.close();
  });

});
