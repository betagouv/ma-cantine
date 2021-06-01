const { getAllDiagnosticsByCanteen } = require("../../infrastructure/repositories/diagnostic");
const { build4YearDiagnostics } = require("../services/diagnostic-builder");

exports.getDiagnosticsByCanteen = async function(canteenId) {
  const diagnostics = await getAllDiagnosticsByCanteen(canteenId);

  return build4YearDiagnostics(diagnostics);
};
