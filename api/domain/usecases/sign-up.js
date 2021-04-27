const { sendLoginLink } = require("../services/authentication");
const { createUserWithCanteen } = require("../../infrastructure/repositories/user");
const { DuplicateUserError } = require("../../infrastructure/errors");

exports.signUp = async function(user, canteen, loginUrl) {
  try {
    await createUserWithCanteen(user, canteen);
  } catch(e) {
    // send login link if user is duplicated
    if(!(e instanceof DuplicateUserError)) {
      throw e;
    }
  }
  await sendLoginLink(user, loginUrl);
}