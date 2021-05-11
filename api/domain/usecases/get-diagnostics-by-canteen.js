const { getAllDiagnosticsByCanteen } = require("../../infrastructure/repositories/diagnostic");

exports.getDiagnosticsByCanteen = async function(canteenId) {
  const dbEntries = await getAllDiagnosticsByCanteen(canteenId);
  return dbEntries.map(entry => {
    let json = entry.toJSON();
    delete json.createdAt;
    delete json.updatedAt;
    delete json.canteenId;
    return json;
  });
};