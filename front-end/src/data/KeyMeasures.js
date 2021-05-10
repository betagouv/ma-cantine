import keyMeasures from "@/data/key-measures.json";

function findSubMeasure(id) {
  for (let measureIdx = 0; measureIdx < keyMeasures.length; measureIdx++) {
    const measure = keyMeasures[measureIdx];
    const subMeasure = measure.subMeasures.find((subMeasure) => subMeasure.id === id);
    if(subMeasure) { return subMeasure; }
  }
}

// TODO: check if data returned by endpoint; if yes create temp restructured version
// if no check local storage
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
      hasDonationAgreement: false,
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
      communicationSupports: [],
      communicationSupportLink: null,
      communicateOnFoodPlan: false,
    },
  };
}

// migration
if(Object.keys(diagnostics["gaspillage-alimentaire"]).indexOf("hasCovenant") !== -1) {
  diagnostics["gaspillage-alimentaire"].hasDonationAgreement = diagnostics["gaspillage-alimentaire"].hasCovenant;
  delete diagnostics["gaspillage-alimentaire"].hasCovenant;
}
if(Object.keys(diagnostics["information-des-usagers"]).indexOf("communicationSupport") !== -1) {
  diagnostics["information-des-usagers"].communicationSupports = diagnostics["information-des-usagers"].communicationSupport;
  delete diagnostics["information-des-usagers"].communicationSupport;
}

// temporary function whilst switching from structured to unstructured,
// TODO: remove once fully moved over
function flattenDiagnostics(diags, defaultYear) {
  let flattened = [{ year: defaultYear }];
  for (const [measureKey, measureData] of Object.entries(diags)) {
    if(measureKey === 'qualite-des-produits') {
      for (const [yearKey, yearData] of Object.entries(measureData)) {
        if(yearKey === defaultYear) {
          flattened[0] = {
            ...flattened[0],
            ...yearData
          };
        } else {
          yearData.year = yearKey;
          flattened.push(yearData);
        }
      }
    } else {
      flattened[0] = {
        ...flattened[0],
        ...measureData
      };
    }
  }
  flattened.forEach(entry => {
    for (const [key, data] of Object.entries(entry)) {
      if(data === null) {
        delete entry[key];
      }
    }
  });
  return flattened;
}

const flattenedDiagnostics = flattenDiagnostics(diagnostics, "2020");

function saveDiagnostic(id, diagnostic) {
  diagnostics[id] = diagnostic;
  localStorage.setItem('diagnostics', JSON.stringify(diagnostics));
}

function haveDiagnosticResults() {
  // TODO: update this
  return !!localStorage.getItem('diagnostics');
}

export {
  keyMeasures,
  findSubMeasure,
  saveDiagnostic,
  diagnostics,
  flattenedDiagnostics,
  haveDiagnosticResults
};
