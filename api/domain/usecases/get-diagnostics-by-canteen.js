const { getAllDiagnosticsByCanteen } = require("../../infrastructure/repositories/diagnostic");

exports.getDiagnosticsByCanteen = async function(canteenId) {
  const dbEntries = await getAllDiagnosticsByCanteen(canteenId);
  const orderedDiagnostics = dbEntries.map(entry => {
    let json = entry.toJSON();
    delete json.createdAt;
    delete json.updatedAt;
    delete json.canteenId;
    return json;
  }).
    sort((earlierDiag, laterDiag) => laterDiag.year - earlierDiag.year);

  let result = {};
  if(orderedDiagnostics.length > 0) {
    result.latest = orderedDiagnostics[0];
  }
  if(orderedDiagnostics.length > 1) {
    result.previous = orderedDiagnostics[1];
  }
  return result;
};