require('../database/setup');
const { Canteen, User } = require('../database/models');

var createCanteen = async function(canteen) {
  return await Canteen.create(canteen);
};

exports.createCanteen = createCanteen;

var createUser = async function(user, canteenId) {
  user.managesCanteen = canteenId;
  return await User.create(user);
};

exports.createUser = createUser;

exports.createUserAndCanteen = async function(request) {
  const canteen = await createCanteen(request.payload.canteen);
  await createUser(request.payload.user, canteen.id)
};
