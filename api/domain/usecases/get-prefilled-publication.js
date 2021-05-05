const { getCanteenById } = require("../../infrastructure/repositories/canteen");
const { getAllDiagnosticsByCanteen } = require("../../infrastructure/repositories/diagnostic");
const { buildPreviousLatestDiagnostics } = require("../services/diagnostic-builder");

exports.getPrefilledPublication = async function(canteenId) {
  const canteen = await getCanteenById(canteenId);
  const diagnostics = await getAllDiagnosticsByCanteen(canteenId);

  return {
    canteen: {
      name: canteen.name,
      city: canteen.city,
      sector: canteen.sector,
    },
    diagnostics: buildPreviousLatestDiagnostics(diagnostics),
  };
};
