const { build4YearDiagnostics } = require("../../../../domain/services/diagnostic-builder");

const defaultDiagnostic = {
  valueBio: null,
  valueFairTrade: null,
  valueSustainable: null,
  valueTotal: null,
  hasMadeWasteDiagnostic: false,
  hasMadeWastePlan: false,
  wasteActions: [],
  hasDonationAgreement: false,
  hasMadeDiversificationPlan: false,
  vegetarianFrequency: null,
  vegetarianMenuType: null,
  cookingFoodContainersSubstituted: false,
  serviceFoodContainersSubstituted: false,
  waterBottlesSubstituted: false,
  disposableUtensilsSubstituted: false,
  communicationSupports: [],
  communicationSupportLink: null,
  communicateOnFoodPlan: false,
};

describe('Diagnostic builder service', () => {
  it('4 year diagnostics returns cleaned and defaulted diagnostics', () => {
    const diagnostics = build4YearDiagnostics([{
      year: 2021,
      createdAt: '1871',
      updatedAt: '2021',
      canteenId: 'super_id'
    }, {
      year: 2019,
    }]);

    expect(diagnostics).toStrictEqual({
      latest: Object.assign({}, defaultDiagnostic, { year: 2020 }),
      previous: { year: 2019 },
      provisionalYear1: { year: 2021 },
      provisionalYear2: Object.assign({}, defaultDiagnostic, { year: 2022 }),
    });
  });
});
