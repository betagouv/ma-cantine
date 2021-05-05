const { buildPreviousLatestDiagnostics } = require("../../../../domain/services/diagnostic-builder");

describe('Diagnostic builder service', () => {
  it('returns cleaned diagnostics', async () => {
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

  it('returns defaults diagnostics', async () => {
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
});
