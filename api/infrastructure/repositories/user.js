require('../postgres-database');
const { createCanteen } = require('./canteen');
const { User } = require('../models/user');

var createUser = function(user, canteenId) {
  user.canteenId = canteenId;
  return User.create(user);
};

var createUserWithCanteen = async function(userPayload, canteenPayload) {
  const canteen = await createCanteen(canteenPayload);
  return createUser(userPayload, canteen.id);
};

var findUser = function(user) {
  return User.findOne({
    where: user
  });
};

module.exports = {
  createUser,
  createUserWithCanteen,
  findUser
}
