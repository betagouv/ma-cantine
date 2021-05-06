const { saveDiagnosticsForCanteen } = require('../../../domain/usecases/save-diagnostics');

jest.mock('../../../infrastructure/repositories/diagnostic');
const { saveDiagnosticForCanteen } = require('../../../infrastructure/repositories/diagnostic');

describe('Save diagnostic usecase', () => {
  it('parses diagnostic payload and triggers save to db', async () => {
    const diagnostic1 = {
      year: 2020,
      valueBio: 40000,
      hasMadeWasteDiagnostic: true,
      hasMadeWastePlan: true,
      vegetarianMenuType: "standalone",
      cookingFoodContainersSubstituted: true,
      communicationSupport: ["email"]
    };
    const diagnostic2 = {
      year: 2019,
      valueBio: 50000
    };
    await saveDiagnosticsForCanteen(90, [diagnostic1, diagnostic2]);
    expect(saveDiagnosticForCanteen).toHaveBeenCalledTimes(2);
    // TODO: should the arguments be: canteenId, year, data ?
    expect(saveDiagnosticForCanteen).toHaveBeenCalledWith(diagnostic1, 90);
    expect(saveDiagnosticForCanteen).toHaveBeenCalledWith(diagnostic2, 90);
  });
});