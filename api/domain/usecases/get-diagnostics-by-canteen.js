const { getAllDiagnosticsByCanteen } = require("../../infrastructure/repositories/diagnostic");

exports.getDiagnosticsByCanteen = function(canteenId) {
  return getAllDiagnosticsByCanteen(canteenId);
};