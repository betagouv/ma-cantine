const { getDiagnosticsByCanteen } = require("../../../domain/usecases/get-diagnostics-by-canteen");

jest.mock("../../../infrastructure/repositories/diagnostic");
const { getAllDiagnosticsByCanteen } = require("../../../infrastructure/repositories/diagnostic");

describe('Get diagnostics by canteen usecase', () => {
  it('calls repository getter', async () => {
    await getDiagnosticsByCanteen(5);

    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(5);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledTimes(1);
  });
});