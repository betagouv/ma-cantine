const { findUserByEmail } = require('../../infrastructure/repositories/user');
const authenticationService = require('../services/authentication');

async function initiateLogin(email, completeLoginUrl) {
  let user;
  try {
    user = await findUserByEmail(email);
  } catch(e) {
    if(e instanceof NotFoundError) {
      return authenticationService.sendSignUpLink(email);
    } else {
      throw e;
    }
  }
  if(user) {
    return authenticationService.sendLoginLink(user, completeLoginUrl);
  }
};
module.exports = {
  initiateLogin
}