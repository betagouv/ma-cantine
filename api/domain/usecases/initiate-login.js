const { getUserByEmail } = require('../../infrastructure/repositories/user');
const authenticationService = require('../services/authentication');
const { NotFoundError } = require('../../infrastructure/errors');

async function initiateLogin(email, completeLoginUrl) {
  let user;
  try {
    user = await getUserByEmail(email);
    return authenticationService.sendLoginLink(user, completeLoginUrl);
  } catch(e) {
    if(e instanceof NotFoundError) {
      return authenticationService.sendSignUpLink(email);
    } else {
      throw e;
    }
  }
};
module.exports = {
  initiateLogin
}