const defaultDiagnostic = function(year) {
  return {
    year,
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
}

function findDiagnosticForYear(diagnostics, year) {
  const diagnostic = diagnostics.find(d => d.year === year);
  return diagnostic || defaultDiagnostic(year);
}

const build4YearDiagnostics = function(diagnostics) {
  const cleanedDiagnostics = diagnostics.map(diagnostic => {
    delete diagnostic.createdAt;
    delete diagnostic.updatedAt;
    delete diagnostic.canteenId;
    return diagnostic;
  });

  return {
    latest: findDiagnosticForYear(cleanedDiagnostics, 2020),
    previous: findDiagnosticForYear(cleanedDiagnostics, 2019),
    provisionalYear1: findDiagnosticForYear(cleanedDiagnostics, 2021),
    provisionalYear2: findDiagnosticForYear(cleanedDiagnostics, 2022),
  }
};

module.exports = {
  build4YearDiagnostics
}
