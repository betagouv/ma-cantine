const { updateCanteen } = require("../../infrastructure/repositories/canteen");

exports.extendCanteenInfos = async function(canteen) {
  return await updateCanteen(canteen);
};
