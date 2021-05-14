const { getDiagnosticsByCanteen } = require("../../../../domain/usecases/get-diagnostics-by-canteen");

jest.mock("../../../../infrastructure/repositories/diagnostic");
const { getAllDiagnosticsByCanteen } = require("../../../../infrastructure/repositories/diagnostic");

jest.mock('../../../../domain/services/diagnostic-builder');
const { buildPreviousLatestDiagnostics } = require('../../../../domain/services/diagnostic-builder');

describe('Get diagnostics by canteen usecase', () => {
  it('returns builded diagnostics', async () => {
    getAllDiagnosticsByCanteen.mockReturnValue(['diag1', 'diag2']);
    buildPreviousLatestDiagnostics.mockReturnValue({});

    const diagnostics = await getDiagnosticsByCanteen(5);

    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(5);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledTimes(1);
    expect(buildPreviousLatestDiagnostics).toHaveBeenCalledWith(['diag1', 'diag2']);
    expect(diagnostics).toStrictEqual({});
  });
});
