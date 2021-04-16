require('../postgres-database');
const { createCanteen } = require('./canteen');
const { User } = require('../models/user');

var createUser = function(user, canteenId) {
  user.canteenId = canteenId;
  return User.create(user);
};

var createUserWithCanteen = async function(request) {
  const canteen = await createCanteen(request.payload.canteen);
  return createUser(request.payload.user, canteen.id);
};

module.exports = {
  createUser,
  createUserWithCanteen
}
