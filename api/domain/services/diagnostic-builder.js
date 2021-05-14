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

const buildPreviousLatestDiagnostics = function(diagnostics) {
  const cleanedDiagnostics = diagnostics.map(diagnostic => {
    delete diagnostic.createdAt;
    delete diagnostic.updatedAt;
    delete diagnostic.canteenId;
    return diagnostic;
  });

  const latest = cleanedDiagnostics.length > 0 ? cleanedDiagnostics[0] : defaultDiagnostic(2020);
  const previous = cleanedDiagnostics.length > 1 ? cleanedDiagnostics[1] : defaultDiagnostic(2019);

  return {
    latest,
    previous
  }
};

module.exports = {
  buildPreviousLatestDiagnostics
}
