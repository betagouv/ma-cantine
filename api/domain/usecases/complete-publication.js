const { getCanteenById, updateCanteen } = require("../../infrastructure/repositories/canteen");

exports.completePublication = async function(canteenId, makeDataPublic) {
  return updateCanteen({ id: canteenId, hasPublished: true, dataIsPublic: makeDataPublic });
};
