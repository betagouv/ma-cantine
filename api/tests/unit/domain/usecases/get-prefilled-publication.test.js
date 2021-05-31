const { getPrefilledPublication } = require('../../../../domain/usecases/get-prefilled-publication')

jest.mock('../../../../infrastructure/repositories/canteen');
const { getCanteenById } = require('../../../../infrastructure/repositories/canteen');

jest.mock('../../../../infrastructure/repositories/diagnostic');
const { getAllDiagnosticsByCanteen } = require('../../../../infrastructure/repositories/diagnostic');

jest.mock('../../../../domain/services/diagnostic-builder');
const { build4YearDiagnostics } = require('../../../../domain/services/diagnostic-builder');

const canteen = {
  id: 3,
  name: "Test canteen",
  city: "Lyon",
  sector: "school",
  mealCount: 150,
  managementType: "conceded"
};

describe('Get prefilled publication', () => {

  beforeAll(() => {
    getAllDiagnosticsByCanteen.mockReturnValue(['diag1', 'diag2']);
    build4YearDiagnostics.mockReturnValue({});
  });

  it('it returns the publication prefilled with diagnostics', async () => {
    getCanteenById.mockReturnValue(canteen);

    const prefilledPublication = await getPrefilledPublication(3);

    expect(getCanteenById).toHaveBeenCalledWith(3);
    expect(getAllDiagnosticsByCanteen).toHaveBeenCalledWith(3);
    expect(build4YearDiagnostics).toHaveBeenCalledWith(['diag1', 'diag2']);
    expect(prefilledPublication).toStrictEqual({
      canteen: {
        name: canteen.name,
        city: canteen.city,
        sector: canteen.sector,
        mealCount: canteen.mealCount,
        siret: canteen.siret,
        managementType: canteen.managementType,
      },
      diagnostics: {}
    });
  });

  it('provides default values', async () => {
    getCanteenById.mockReturnValue({ id: 3 });

    const prefilledPublication = await getPrefilledPublication(3);

    expect(prefilledPublication.canteen.managementType).toBe('direct');
  });
});
