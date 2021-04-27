require('../postgres-database');
const { createCanteen } = require('./canteen');
const { User } = require('../models/user');

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
      user = await findUser({ email: userPayload.email });
    } else {
      throw e;
    }
  }
  return user;
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
