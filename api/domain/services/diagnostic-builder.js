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

function cleanDiagnostics(diagnostics) {
  return diagnostics.map(diagnostic => {
    delete diagnostic.createdAt;
    delete diagnostic.updatedAt;
    delete diagnostic.canteenId;
    return diagnostic;
  });
}

function findDiagnosticForYear(diagnostics, year) {
  const diagnostic = diagnostics.find(d => d.year === year);
  return diagnostic || defaultDiagnostic(year);
}

const buildPreviousLatestDiagnostics = function(diagnostics) {
  const cleanedDiagnostics = cleanDiagnostics(diagnostics);

  return {
    latest: findDiagnosticForYear(cleanedDiagnostics, 2020),
    previous: findDiagnosticForYear(cleanedDiagnostics, 2019),
  }
};

const build4YearDiagnostics = function(diagnostics) {
  const cleanedDiagnostics = cleanDiagnostics(diagnostics);

  return {
    latest: findDiagnosticForYear(cleanedDiagnostics, 2020),
    previous: findDiagnosticForYear(cleanedDiagnostics, 2019),
    provisionalYear1: findDiagnosticForYear(cleanedDiagnostics, 2021),
    provisionalYear2: findDiagnosticForYear(cleanedDiagnostics, 2022),
  }
};

module.exports = {
  buildPreviousLatestDiagnostics,
  build4YearDiagnostics
}
