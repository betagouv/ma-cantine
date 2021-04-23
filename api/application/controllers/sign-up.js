const { initiateMagicLinkLogin } = require("../../domain/usecases/login");
const { createUserWithCanteen } = require("../../infrastructure/repositories/user");

exports.signUp = async function(request, h) {
  const user = request.payload.user;
  const canteen = request.payload.canteen;
  const createdUser = await createUserWithCanteen(user, canteen);
  initiateMagicLinkLogin(createdUser.email);
  return h.response().code(201);
};