const { getDiagnosticsByCanteen } = require("../../../domain/usecases/get-diagnostics-by-canteen");

jest.mock("../../../infrastructure/repositories/diagnostic");
const { getAllDiagnosticsByCanteen } = require("../../../infrastructure/repositories/diagnostic");

describe('Get diagnostics by canteen usecase', () => {
  it('returns results from repository getter', async () => {
    getAllDiagnosticsByCanteen.mockReturnValue([{ year: 2030, valueBio: 600 }]);

    const diagnostics = await getDiagnosticsByCanteen(5);

    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(5);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledTimes(1);
    expect(diagnostics).toStrictEqual([{ year: 2030, valueBio: 600 }]);
  });
});