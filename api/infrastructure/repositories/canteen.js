require('../postgres-database');
const { Canteen } = require('../models/canteen');
const { NotFoundError } = require("../../infrastructure/errors");

// what about duplicate canteens?
const createCanteen = function(canteen) {
  return Canteen.create(canteen);
};

const updateCanteen = async function(canteen) {
  return Canteen.update(canteen, { where: { id: canteen.id } });
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
  updateCanteen,
  getCanteenById
}
