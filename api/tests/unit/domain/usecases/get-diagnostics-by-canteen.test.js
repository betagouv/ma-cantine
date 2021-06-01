const { getDiagnosticsByCanteen } = require("../../../../domain/usecases/get-diagnostics-by-canteen");

jest.mock("../../../../infrastructure/repositories/diagnostic");
const { getAllDiagnosticsByCanteen } = require("../../../../infrastructure/repositories/diagnostic");

jest.mock('../../../../domain/services/diagnostic-builder');
const { build4YearDiagnostics } = require('../../../../domain/services/diagnostic-builder');

describe('Get diagnostics by canteen usecase', () => {
  it('returns builded diagnostics', async () => {
    getAllDiagnosticsByCanteen.mockReturnValue(['diag1', 'diag2']);
    build4YearDiagnostics.mockReturnValue({});

    const diagnostics = await getDiagnosticsByCanteen(5);

    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(5);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledTimes(1);
    expect(build4YearDiagnostics).toHaveBeenCalledWith(['diag1', 'diag2']);
    expect(diagnostics).toStrictEqual({});
  });
});
