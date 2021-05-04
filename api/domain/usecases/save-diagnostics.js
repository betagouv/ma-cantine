const { saveDiagnosticForCanteen } = require("../../infrastructure/repositories/diagnostic");

exports.saveDiagnosticsForUser = async function(user, diagnostics) {
  diagnostics.forEach(async (diagnostic) => {
    await saveDiagnosticForCanteen(diagnostic, user.canteenId);
  });
};