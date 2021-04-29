require('../postgres-database');
const { createCanteen } = require('./canteen');
const { User } = require('../models/user');
const { NotFoundError } = require("../../infrastructure/errors");

var createUser = function(user, canteenId) {
  user.canteenId = canteenId;
  return User.create(user);
};

var createUserWithCanteen = async function(userPayload, canteenPayload) {
  const canteen = await createCanteen(canteenPayload);
  let user;
  try {
    user = await createUser(userPayload, canteen.id);
  } catch(e) {
    await canteen.destroy();
    if(e.name === 'SequelizeUniqueConstraintError' && e.errors[0].path === 'email') {
      user = await getUserByEmail(userPayload.email);
    } else {
      throw e;
    }
  }
  return user;
};

var getUserByEmail = async function(email) {
  const user = await User.findOne({
    where: {
      email
    }
  });
  if(!user) {
    throw new NotFoundError("No user for email: " + email);
  }
  return user;
};

module.exports = {
  createUser,
  createUserWithCanteen,
  getUserByEmail
}
