const { getAllDiagnosticsByCanteen } = require("../../infrastructure/repositories/diagnostic");
const { buildPreviousLatestDiagnostics } = require("../services/diagnostic-builder");

exports.getDiagnosticsByCanteen = async function(canteenId) {
  const diagnostics = await getAllDiagnosticsByCanteen(canteenId);

  return buildPreviousLatestDiagnostics(diagnostics);
};
