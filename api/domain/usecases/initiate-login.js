const { findUser } = require('../../infrastructure/repositories/user');
const authenticationService = require('../services/authentication');

async function initiateLogin(email, completeLoginUrl) {
  let user = await findUser({ email: email });
  if(user) {
    await authenticationService.sendLoginLink(user, completeLoginUrl);
  } else {
    authenticationService.sendSignUpLink(email);
  }
};

module.exports = {
  initiateLogin
}