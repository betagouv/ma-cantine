import keyMeasures from "@/data/key-measures.json";

function findSubMeasure(id) {
  for (let measureIdx = 0; measureIdx < keyMeasures.length; measureIdx++) {
    const measure = keyMeasures[measureIdx];
    const subMeasure = measure.subMeasures.find((subMeasure) => subMeasure.id === id);
    if(subMeasure) { return subMeasure; }
  }
}

const defaultDiagnostics = {
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

const defaultFlatDiagnostic = {
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

const defaultFlatDiagnostics = [defaultFlatDiagnostic];

async function getDiagnostics() {
  let flatDiagnostics, hasSavedResults;
  let diagnostics = defaultDiagnostics;

  const jwt = localStorage.getItem('jwt');
  if(jwt) {
    const response = await fetch(`${process.env.VUE_APP_API_URL}/get-diagnostics-by-canteen`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+jwt
      }
    });
    if(response.status === 200) {
      flatDiagnostics = await response.json();
      diagnostics = restructureDiagnostics(flatDiagnostics);
      hasSavedResults = true;
    }
    // TODO: remove jwt from local if 401 ?
  }

  const localDiagnostics = getLocalDiagnostics();

  if(!flatDiagnostics) {
    diagnostics = localDiagnostics.diagnostics;
    flatDiagnostics = localDiagnostics.flatDiagnostics;
  }

  return {
    diagnostics,
    flatDiagnostics,
    localFlatDiagnostics: localDiagnostics.flatDiagnostics,
    hasResults: hasSavedResults || !!localStorage.getItem('diagnostics')
  };
}

function getLocalDiagnostics() {
  let diagnostics = defaultDiagnostics;
  let flatDiagnostics;
  const diagnosticsString = localStorage.getItem('diagnostics');
  if(diagnosticsString) {
    diagnostics = JSON.parse(diagnosticsString);
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

  flatDiagnostics = flattenDiagnostics(diagnostics, "2020");
  return { diagnostics, flatDiagnostics };
}

// TODO: remove this once all diagnostic usage points to flat diagnostics
function restructureDiagnostics(flatDiagnostics) {
  const previousYear = flatDiagnostics.find(diagnostic => diagnostic.year === 2019) || defaultFlatDiagnostic;
  const currentYear = flatDiagnostics.find(diagnostic => diagnostic.year === 2020) || defaultFlatDiagnostic;
  return {
    "qualite-des-produits": {
      "2019": {
        valueBio: previousYear.valueBio,
        valueFairTrade: previousYear.valueFairTrade,
        valueSustainable: previousYear.valueSustainable,
        valueTotal: previousYear.valueTotal,
      },
      "2020": {
        valueBio: currentYear.valueBio,
        valueFairTrade: currentYear.valueFairTrade,
        valueSustainable: currentYear.valueSustainable,
        valueTotal: currentYear.valueTotal,
      }
    },
    "gaspillage-alimentaire": {
      hasMadeWasteDiagnostic: currentYear.hasMadeWasteDiagnostic,
      hasMadeWastePlan: currentYear.hasMadeWastePlan,
      wasteActions: currentYear.wasteActions,
      hasDonationAgreement: currentYear.hasDonationAgreement,
    },
    "diversification-des-menus": {
      hasMadeDiversificationPlan: currentYear.hasMadeDiversificationPlan,
      vegetarianFrequency: currentYear.vegetarianFrequency,
      vegetarianMenuType: currentYear.vegetarianMenuType,
    },
    "interdiction-du-plastique": {
      cookingFoodContainersSubstituted: currentYear.cookingFoodContainersSubstituted,
      serviceFoodContainersSubstituted: currentYear.serviceFoodContainersSubstituted,
      waterBottlesSubstituted: currentYear.waterBottlesSubstituted,
      disposableUtensilsSubstituted: currentYear.disposableUtensilsSubstituted,
    },
    "information-des-usagers": {
      communicationSupports: currentYear.communicationSupports,
      communicationSupportLink: currentYear.communicationSupportLink,
      communicateOnFoodPlan: currentYear.communicateOnFoodPlan,
    },
  }
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
      if(data === null || data === "") {
        delete entry[key];
      } else if(['year', 'valueBio', 'valueFairTrade', 'valueSustainable', 'valueTotal'].indexOf(key) !== -1) {
        entry[key] = parseInt(data, 10);
      }
    }
  });
  return flattened;
}

async function saveDiagnostic(id, diagnostic) {
  const { diagnostics } = await getDiagnostics();
  diagnostics[id] = diagnostic;
  localStorage.setItem('diagnostics', JSON.stringify(diagnostics));
}

async function haveDiagnosticResults() {
  return (await getDiagnostics()).hasResults;
}

const diagnostics = {};

export {
  keyMeasures,
  findSubMeasure,
  saveDiagnostic,
  getDiagnostics,
  haveDiagnosticResults,
  // TODO: review the following
  diagnostics,
  defaultFlatDiagnostic,
  defaultFlatDiagnostics
};
