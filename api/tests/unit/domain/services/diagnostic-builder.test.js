const { buildPreviousLatestDiagnostics, build4YearDiagnostics } = require("../../../../domain/services/diagnostic-builder");

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
  it('previousLatestDiagnostics returns cleaned diagnostics', async () => {
    const diagnostics = buildPreviousLatestDiagnostics([{
      year: 2020,
      createdAt: '1871',
      updatedAt: '2021',
      canteenId: 'super_id'
    }, {
      year: 2019,
    }]);

    expect(diagnostics).toStrictEqual({
      latest: { year: 2020 },
      previous: { year: 2019 }
    });
  });

  it('previousLatestDiagnostics returns defaults diagnostics', async () => {
    const diagnostics = buildPreviousLatestDiagnostics([]);

    expect(diagnostics).toStrictEqual({
      latest: {
        year: 2020,
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
      },
      previous: {
        year: 2019,
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
      }
    });
  });

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
