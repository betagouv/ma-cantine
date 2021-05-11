const { getDiagnosticsByCanteen } = require("../../../domain/usecases/get-diagnostics-by-canteen");

jest.mock("../../../infrastructure/repositories/diagnostic");
const { getAllDiagnosticsByCanteen } = require("../../../infrastructure/repositories/diagnostic");

describe('Get diagnostics by canteen usecase', () => {
  it('returns results from repository getter, removing db-specific keys', async () => {
    getAllDiagnosticsByCanteen.mockReturnValue([{
      toJSON() {
        return {
          year: 2030,
          valueBio: 600,
          createdAt: "2020-08-01",
          updatedAt: "2020-08-01",
          canteenId: 5
        };
      }
    }]);

    const diagnostics = await getDiagnosticsByCanteen(5);

    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(5);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledTimes(1);
    expect(diagnostics).toStrictEqual([{ year: 2030, valueBio: 600 }]);
  });
});