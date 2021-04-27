const { sendLoginLink } = require("../services/authentication");
const { createUserWithCanteen } = require("../../infrastructure/repositories/user");

exports.signUp = async function(user, canteen, loginUrl) {
  const userEntry = await createUserWithCanteen(user, canteen);
  await sendLoginLink(userEntry, loginUrl);
}