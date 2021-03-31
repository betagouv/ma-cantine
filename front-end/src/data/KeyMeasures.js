import keyMeasures from "@/data/key-measures.json";

function saveStatus(id, status) {
  const statuses = JSON.parse(localStorage.getItem('statuses') || '{}');
  statuses[id] = status;
  localStorage.setItem('statuses', JSON.stringify(statuses));
}

const statusesString = localStorage.getItem('statuses') || "{}";
const statuses = JSON.parse(statusesString);

keyMeasures.forEach(measure => {
  measure.subMeasures.forEach(subMeasure => {
    subMeasure.status = statuses[subMeasure.id];
  });
});

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
    "information-des-usagers": {
      communicationSupport: [],
      communicationSupportLink: null,
      communicateOnFoodPlan: false,
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
    }
  };
}

function saveDiagnostic(id, diagnostic) {
  diagnostics[id] = diagnostic;
  localStorage.setItem('diagnostics', JSON.stringify(diagnostics));
}

export {
  keyMeasures,
  saveStatus,
  findSubMeasure,
  saveDiagnostic,
  diagnostics
};
