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

const getAllDiagnosticsByCanteen = async function(canteenId) {
  const diagnostics = await Diagnostic.findAll({
    where: {
      canteenId
    },
    order: [
      ['year', 'DESC'],
    ],
  });
  return diagnostics.map(diagnostic => diagnostic.toJSON());
};

module.exports = {
  saveDiagnosticsForCanteen,
  getAllDiagnosticsByCanteen
}
