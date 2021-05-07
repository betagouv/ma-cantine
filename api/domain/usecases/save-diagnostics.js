const { saveDiagnosticsForCanteen } = require("../../infrastructure/repositories/diagnostic");

exports.saveDiagnosticsForCanteen = function(canteenId, diagnostics) {
  return saveDiagnosticsForCanteen(canteenId, diagnostics);
};