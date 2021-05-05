const { getPrefilledPublication } = require('../../../domain/usecases/get-prefilled-publication')

jest.mock('../../../infrastructure/repositories/canteen');
const { getCanteenById } = require('../../../infrastructure/repositories/canteen');

jest.mock('../../../infrastructure/repositories/diagnostic');
const { getAllDiagnosticsByCanteen } = require('../../../infrastructure/repositories/diagnostic');

jest.mock('../../../domain/services/diagnostic-builder');
const { buildPreviousLatestDiagnostics } = require('../../../domain/services/diagnostic-builder');

const canteen = {
  id: 3,
  name: "Test canteen",
  city: "Lyon",
  sector: "school"
};

describe('Get prefilled publication', () => {
  it('it returns the publication prefilled with diagnostics', async () => {
    getCanteenById.mockReturnValue(canteen);
    getAllDiagnosticsByCanteen.mockReturnValue(['diag1', 'diag2']);
    buildPreviousLatestDiagnostics.mockReturnValue({});

    const prefilledPublication = await getPrefilledPublication(3);

    expect(getCanteenById).toHaveBeenCalledWith(3);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(3);
    expect(buildPreviousLatestDiagnostics).toHaveBeenCalledWith(['diag1', 'diag2']);
    expect(prefilledPublication).toStrictEqual({
      canteen: {
        name: canteen.name,
        city: canteen.city,
        sector: canteen.sector,
      },
      diagnostics: {}
    });
  });
});
