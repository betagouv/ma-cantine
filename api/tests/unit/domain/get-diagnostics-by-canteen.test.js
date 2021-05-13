const { getDiagnosticsByCanteen } = require("../../../domain/usecases/get-diagnostics-by-canteen");

jest.mock("../../../infrastructure/repositories/diagnostic");
const { getAllDiagnosticsByCanteen } = require("../../../infrastructure/repositories/diagnostic");

describe('Get diagnostics by canteen usecase', () => {
  it('returns latest and previous diagnostic, removing db-specific keys', async () => {
    getAllDiagnosticsByCanteen.mockReturnValue([
      {
        toJSON() {
          return {
            year: 2030,
            valueBio: 600,
            createdAt: "2020-08-01",
            updatedAt: "2020-08-01",
            canteenId: 5
          };
        }
      },
      {
        toJSON() {
          return {
            year: 2031,
            valueBio: 700,
            createdAt: "2020-08-01",
            updatedAt: "2020-08-01",
            canteenId: 5
          };
        }
      },
      {
        toJSON() {
          return {
            year: 2029,
            valueBio: 800,
            createdAt: "2020-08-01",
            updatedAt: "2020-08-01",
            canteenId: 5
          };
        }
      }
    ]);

    const diagnostics = await getDiagnosticsByCanteen(5);

    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(5);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledTimes(1);
    expect(diagnostics).toStrictEqual({
      latest: { year: 2031, valueBio: 700 },
      previous: { year: 2030, valueBio: 600 }
    });
  });

  it('only returns object with latest key, if canteen has just one entry', async () => {
    getAllDiagnosticsByCanteen.mockReturnValue([{
      toJSON() {
        return { year: 2030, valueBio: 5 };
      }
    }]);
    const diagnostics = await getDiagnosticsByCanteen(5);
    expect(diagnostics).toStrictEqual({ latest: { year: 2030, valueBio: 5 } });
  });

  it('returns empty object, if canteen has no entries', async () => {
    getAllDiagnosticsByCanteen.mockReturnValue([]);
    const diagnostics = await getDiagnosticsByCanteen(5);
    expect(diagnostics).toStrictEqual({});
  });
});