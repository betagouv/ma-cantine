require('../postgres-database');
const { Canteen } = require('../models/canteen');

// what about duplicate canteens?
exports.createCanteen = function(canteen) {
  return Canteen.create(canteen);
};
