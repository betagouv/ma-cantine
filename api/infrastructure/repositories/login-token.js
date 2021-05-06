const { NotFoundError } = require('../errors');
const { LoginToken } = require('../models/login-token');
const { User } = require('../models/user');

var saveLoginTokenForUser = async function(user, token) {
  await LoginToken.destroy({
    where: {
      userId: user.id
    }
  });
  return LoginToken.create({
    token: token,
    userId: user.id
  });
};

var getUserForLoginToken = async function(token) {
  let tokenEntry = await LoginToken.findOne({
    where: {
      token
    },
    include: User
  });
  let user;
  if(tokenEntry) {
    if(new Date(tokenEntry.expirationDate) > new Date()) {
      user = tokenEntry.user;
    }
    await tokenEntry.destroy();
  }
  if(!user) {
    throw new NotFoundError("No login token: " + token);
  }
  return user;
};

module.exports = {
  saveLoginTokenForUser,
  getUserForLoginToken
};
