require('../postgres-database');
const { createCanteen } = require('./canteen');
const { User } = require('../models/user');

class DuplicateUserError extends Error {};

var createUser = function(user, canteenId) {
  user.canteenId = canteenId;
  return User.create(user);
};

// TODO: avoid creating a canteen if the user fails to create (e.g. duplicate email)
var createUserWithCanteen = async function(userPayload, canteenPayload) {
  const canteen = await createCanteen(canteenPayload);
  try {
    return (await createUser(userPayload, canteen.id));
  } catch(e) {
    if(e.name === 'SequelizeUniqueConstraintError' && e.errors[0].path === 'email') {
      throw new DuplicateUserError();
    } else {
      throw e;
    }
  }
};

var findUser = function(user) {
  return User.findOne({
    where: user
  });
};

module.exports = {
  createUser,
  createUserWithCanteen,
  findUser,
  DuplicateUserError
}
