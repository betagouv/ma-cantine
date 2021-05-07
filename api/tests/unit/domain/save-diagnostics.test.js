const { saveDiagnosticsForCanteen: saveDiagnosticsForCanteenUsecase } = require('../../../domain/usecases/save-diagnostics');

jest.mock('../../../infrastructure/repositories/diagnostic');
const { saveDiagnosticsForCanteen } = require('../../../infrastructure/repositories/diagnostic');

describe('Save diagnostic usecase', () => {
  it('triggers save of diagnostics to database', async () => {
    const diagnostics = [
      { year: 2020, vegetarianMenuType: "standalone" },
      { year: 2019, valueBio: 50000 }
    ];
    await saveDiagnosticsForCanteenUsecase(90, diagnostics);
    expect(saveDiagnosticsForCanteen).toHaveBeenCalledTimes(1);
    expect(saveDiagnosticsForCanteen).toHaveBeenCalledWith(90, diagnostics);
  });
});