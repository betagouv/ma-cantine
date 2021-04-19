const { LoginToken } = require('../models/login-token');

var saveTokenForUser = async function(user, token) {
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

var getValidToken = async function(user) {
  let token = await LoginToken.findOne({
    where: {
      userId: user.id
    }
  });
  if(new Date(token.expirationDate) > new Date()) {
    return token.token;
  } else {
    token.destroy();
  }
};

module.exports = {
  saveTokenForUser,
  getValidToken
};