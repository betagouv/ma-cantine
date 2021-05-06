const { saveDiagnosticForCanteen } = require("../../infrastructure/repositories/diagnostic");

exports.saveDiagnosticsForCanteen = async function(canteenId, diagnostics) {
  diagnostics.forEach(async (diagnostic) => {
    await saveDiagnosticForCanteen(diagnostic, canteenId);
  });
};