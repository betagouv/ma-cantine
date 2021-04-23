const { initiateMagicLinkLogin } = require("../../domain/usecases/login");
const { createUserWithCanteen } = require("../../infrastructure/repositories/user");

// TODO: fail with 400 for badly formatted request payload
exports.signUp = async function(request, h) {
  let code;
  const user = request.payload.user;
  const canteen = request.payload.canteen;
  const createdUser = await createUserWithCanteen(user, canteen);
  if(createdUser) {
    code = 201;
    initiateMagicLinkLogin(createdUser.email);
  } else {
    code = 400;
  }
  return h.response().code(code);
};