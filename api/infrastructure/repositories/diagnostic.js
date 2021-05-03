require('../postgres-database');
const { NotFoundError } = require("../../infrastructure/errors");
const { Diagnostic } = require('../models/diagnostic');

const saveDiagnosticForCanteen = async function(data, canteenId) {
  data.canteenId = canteenId;
  let diagnostic;
  try {
    diagnostic = await Diagnostic.upsert(data);
  } catch(e) {
    if(e.name === 'SequelizeForeignKeyConstraintError') {
      throw new NotFoundError("Error when saving diagnostic, no canteen found for id: " + canteenId);
    } else {
      throw e;
    }
  }
  return diagnostic[0];
};

const getAllDiagnosticsByCanteen = function(canteenId) {
  return Diagnostic.findAll({
    where: {
      canteenId
    }
  });
};

module.exports = {
  saveDiagnosticForCanteen,
  getAllDiagnosticsByCanteen
}
