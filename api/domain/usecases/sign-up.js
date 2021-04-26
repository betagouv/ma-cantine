const { initiateMagicLinkLogin } = require("../services/initiate-login");
const { createUserWithCanteen, DuplicateUserError } = require("../../infrastructure/repositories/user");

exports.signUp = async function(user, canteen) {
  try {
    await createUserWithCanteen(user, canteen);
  } catch(e) {
    // send login link if user is duplicated
    if(!(e instanceof DuplicateUserError)) {
      throw e;
    }
  }
  initiateMagicLinkLogin(user.email);
}