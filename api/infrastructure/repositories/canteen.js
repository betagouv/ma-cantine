require('../postgres-database');
const { Canteen } = require('../models/canteen');

exports.createCanteen = function(canteen) {
  return Canteen.create(canteen);
};
