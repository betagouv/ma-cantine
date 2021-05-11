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

function defaultFlatDiagnosticWithYear(diagnostic, year) {
  let diagnosticCopy = JSON.parse(JSON.stringify(diagnostic));
  diagnosticCopy.year = year;
  return diagnosticCopy;
}

const defaultFlatDiagnostics = [
  defaultFlatDiagnosticWithYear(defaultFlatDiagnostic, 2019),
  defaultFlatDiagnosticWithYear(defaultFlatDiagnostic, 2020)
];

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
  let flatDiagnostics = defaultFlatDiagnostics;
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

  flatDiagnostics = flattenDiagnostics(diagnostics, 2020);
  return { diagnostics, flatDiagnostics };
}

// temporary functions whilst switching from structured to unstructured
// TODO: remove this once all diagnostic usage points to flat diagnostics
function restructureDiagnostics(flatDiagnostics) {
  const previousDiagnostic = findPreviousDiagnostic(flatDiagnostics) || defaultFlatDiagnostic;
  const latestDiagnostic = findLatestDiagnostic(flatDiagnostics) || defaultFlatDiagnostic;
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
        const year = parseInt(yearKey, 10);
        if(year === defaultYear) {
          flattened[0] = {
            ...flattened[0],
            ...yearData
          };
        } else {
          yearData.year = year;
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
  return cleanDiagnostics(flattened);
}

function cleanDiagnostics(flatDiagnostics) {
  flatDiagnostics.forEach(entry => {
    for (const [key, data] of Object.entries(entry)) {
      // TODO: endpoint probably shouldn't send db keys in the first place
      if(data === null || data === "" || ['createdAt', 'updatedAt', 'canteenId'].indexOf(key) !== -1) {
        delete entry[key];
      } else if(key === 'year') {
        // expect year to be number
        entry[key] = parseInt(entry[key], 10);
      }
    }
  });
  return flatDiagnostics;
}

async function saveDiagnostic(diagnostic) {
  const { flatDiagnostics } = await getDiagnostics();
  let diagnostics = flatDiagnostics;
  const idx = diagnostics.findIndex(d => d.year === diagnostic.year);
  // at the moment, the diagnostics are defaulted to guarantee a year match
  diagnostics[idx] = diagnostic;
  return saveDiagnostics(diagnostics);
}

async function saveDiagnostics(diagnostics) {
  diagnostics = cleanDiagnostics(diagnostics);
  let isSaved = false;
  const jwt = localStorage.getItem('jwt');
  if(jwt) {
    const response = await fetch(`${process.env.VUE_APP_API_URL}/save-diagnostics`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+jwt
      },
      body: JSON.stringify({
        diagnostics
      })
    });
    if(response.status === 201) {
      isSaved = true;
    }
  }

  if(!isSaved) {
    localStorage.setItem('diagnostics', JSON.stringify(restructureDiagnostics(diagnostics)));
  }
}

function findLatestDiagnostic(diagnostics) {
  return diagnostics.find(diagnostic => diagnostic.year === 2020);
}

function findPreviousDiagnostic(diagnostics) {
  return diagnostics.find(diagnostic => diagnostic.year === 2019);
}

export {
  keyMeasures,
  findSubMeasure,
  saveDiagnostic,
  saveDiagnostics,
  getDiagnostics,
  defaultFlatDiagnostic,
  defaultFlatDiagnostics,
  findLatestDiagnostic,
  findPreviousDiagnostic
};
