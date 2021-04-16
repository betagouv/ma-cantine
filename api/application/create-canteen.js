require('../database/setup');
const { Canteen } = require('../database/models');

exports.createCanteen = function(canteen) {
  return Canteen.create(canteen);
};
