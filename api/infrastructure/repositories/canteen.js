require('../postgres-database');
const { Canteen } = require('../models/canteen');
const { NotFoundError } = require("../../infrastructure/errors");

// what about duplicate canteens?
const createCanteen = function(canteen) {
  return Canteen.create(canteen);
};

const getCanteenById = async function(id) {
  const canteen = await Canteen.findOne({ where: { id } });

  if(!canteen) {
    throw new NotFoundError("No canteen for id: " + id);
  }

  return canteen;
};

module.exports = {
  createCanteen,
  getCanteenById
}
