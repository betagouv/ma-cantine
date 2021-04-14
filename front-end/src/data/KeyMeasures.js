import keyMeasures from "@/data/key-measures.json";

function findSubMeasure(id) {
  for (let measureIdx = 0; measureIdx < keyMeasures.length; measureIdx++) {
    const measure = keyMeasures[measureIdx];
    const subMeasure = measure.subMeasures.find((subMeasure) => subMeasure.id === id);
    if(subMeasure) { return subMeasure; }
  }
}

const diagnosticsString = localStorage.getItem('diagnostics');
let diagnostics = {};
if (diagnosticsString) {
  diagnostics = JSON.parse(diagnosticsString);
} else {
  diagnostics = {
    "qualite-des-produits": {
      "2019": {
        valueBio: null,
        valueFairTrade: null,
        valueSustainable: null,
        valueTotal: null,
      },
      "2020": {
        valueBio: null,
        valueFairTrade: null,
        valueSustainable: null,
        valueTotal: null,
      }
    },
    "gaspillage-alimentaire": {
      hasMadeWasteDiagnostic: false,
      hasMadeWastePlan: false,
      wasteActions: [],
      hasCovenant: false,
    },
    "diversification-des-menus": {
      hasMadeDiversificationPlan: false,
      vegetarianFrequency: null,
      vegetarianMenuType: null,
    },
    "interdiction-du-plastique": {
      cookingFoodContainersSubstituted: false,
      serviceFoodContainersSubstituted: false,
      waterBottlesSubstituted: false,
      disposableUtensilsSubstituted: false,
    },
    "information-des-usagers": {
      communicationSupport: [],
      communicationSupportLink: null,
      communicateOnFoodPlan: false,
    },
  };
}

function saveDiagnostic(id, diagnostic) {
  diagnostics[id] = diagnostic;
  localStorage.setItem('diagnostics', JSON.stringify(diagnostics));
}

function haveDiagnosticResults() {
  return !!localStorage.getItem('diagnostics');
}

export {
  keyMeasures,
  findSubMeasure,
  saveDiagnostic,
  diagnostics,
  haveDiagnosticResults
};
