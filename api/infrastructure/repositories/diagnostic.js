require('../postgres-database');
const { NotFoundError } = require("../../infrastructure/errors");
const { Diagnostic } = require('../models/diagnostic');

const saveDiagnosticsForCanteen = async function(canteenId, diagnostics) {
  diagnostics.forEach(diagnostic => {
    diagnostic.canteenId = canteenId;
  });
  const modelAttributes = await Diagnostic.describe();
  try {
    await Diagnostic.bulkCreate(diagnostics, {
      updateOnDuplicate: Object.keys(modelAttributes)
    });
  } catch(e) {
    if(e.name === 'SequelizeForeignKeyConstraintError') {
      throw new NotFoundError("Error when saving diagnostic, no canteen found for id: " + canteenId);
    } else {
      throw e;
    }
  }
};

const getAllDiagnosticsByCanteen = function(canteenId) {
  return Diagnostic.findAll({
    where: {
      canteenId
    }
  });
};

module.exports = {
  saveDiagnosticsForCanteen,
  getAllDiagnosticsByCanteen
}
