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

  const flatDiagnostics = flattenDiagnostics(diagnostics, "2020");
  return { diagnostics, flatDiagnostics };
}

// temporary functions whilst switching from structured to unstructured
// TODO: remove this once all diagnostic usage points to flat diagnostics
function restructureDiagnostics(flatDiagnostics) {
  const previousDiagnostic = flatDiagnostics.find(diagnostic => diagnostic.year === 2019) || defaultFlatDiagnostic;
  const latestDiagnostic = flatDiagnostics.find(diagnostic => diagnostic.year === 2020) || defaultFlatDiagnostic;
  return {
    "qualite-des-produits": {
      "2019": {
        valueBio: previousDiagnostic.valueBio,
        valueFairTrade: previousDiagnostic.valueFairTrade,
        valueSustainable: previousDiagnostic.valueSustainable,
        valueTotal: previousDiagnostic.valueTotal,
      },
      "2020": {
        valueBio: latestDiagnostic.valueBio,
        valueFairTrade: latestDiagnostic.valueFairTrade,
        valueSustainable: latestDiagnostic.valueSustainable,
        valueTotal: latestDiagnostic.valueTotal,
      }
    },
    "gaspillage-alimentaire": {
      hasMadeWasteDiagnostic: latestDiagnostic.hasMadeWasteDiagnostic,
      hasMadeWastePlan: latestDiagnostic.hasMadeWastePlan,
      wasteActions: latestDiagnostic.wasteActions,
      hasDonationAgreement: latestDiagnostic.hasDonationAgreement,
    },
    "diversification-des-menus": {
      hasMadeDiversificationPlan: latestDiagnostic.hasMadeDiversificationPlan,
      vegetarianFrequency: latestDiagnostic.vegetarianFrequency,
      vegetarianMenuType: latestDiagnostic.vegetarianMenuType,
    },
    "interdiction-du-plastique": {
      cookingFoodContainersSubstituted: latestDiagnostic.cookingFoodContainersSubstituted,
      serviceFoodContainersSubstituted: latestDiagnostic.serviceFoodContainersSubstituted,
      waterBottlesSubstituted: latestDiagnostic.waterBottlesSubstituted,
      disposableUtensilsSubstituted: latestDiagnostic.disposableUtensilsSubstituted,
    },
    "information-des-usagers": {
      communicationSupports: latestDiagnostic.communicationSupports,
      communicationSupportLink: latestDiagnostic.communicationSupportLink,
      communicateOnFoodPlan: latestDiagnostic.communicateOnFoodPlan,
    },
  }
}

// TODO: remove with restructureDiagnostics once possible
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

const defaultFlatDiagnostics = [defaultFlatDiagnostic];

export {
  keyMeasures,
  findSubMeasure,
  saveDiagnostic,
  getDiagnostics,
  defaultFlatDiagnostic,
  defaultFlatDiagnostics
};
