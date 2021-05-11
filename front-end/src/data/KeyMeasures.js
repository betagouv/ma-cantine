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
      hasSavedResults = true;
    }
  }

  const localDiagnostics = getLocalDiagnostics();

  if(!flatDiagnostics) {
    flatDiagnostics = localDiagnostics.flatDiagnostics;
  }

  return {
    flatDiagnostics,
    localFlatDiagnostics: localDiagnostics.flatDiagnostics,
    hasResults: hasSavedResults || !!localStorage.getItem(LOCAL_FLAT_KEY) || !!localStorage.getItem('diagnostics')
  };
}

const LOCAL_FLAT_KEY = 'flatDiagnostics';

function getLocalDiagnostics() {
  let diagnostics = defaultDiagnostics;
  let flatDiagnostics = defaultFlatDiagnostics;
  const diagnosticsString = localStorage.getItem(LOCAL_FLAT_KEY) || localStorage.getItem('diagnostics');
  if(diagnosticsString) {
    diagnostics = JSON.parse(diagnosticsString);
  }

  // TODO: remove when our testers are using the new structure
  if(!localStorage.getItem(LOCAL_FLAT_KEY)) {
    if(Object.keys(diagnostics["gaspillage-alimentaire"]).indexOf("hasCovenant") !== -1) {
      diagnostics["gaspillage-alimentaire"].hasDonationAgreement = diagnostics["gaspillage-alimentaire"].hasCovenant;
      delete diagnostics["gaspillage-alimentaire"].hasCovenant;
    }
    if(Object.keys(diagnostics["information-des-usagers"]).indexOf("communicationSupport") !== -1) {
      diagnostics["information-des-usagers"].communicationSupports = diagnostics["information-des-usagers"].communicationSupport;
      delete diagnostics["information-des-usagers"].communicationSupport;
    }
    flatDiagnostics = flattenDiagnostics(diagnostics, 2020);
  } else {
    flatDiagnostics = diagnostics;
  }

  return { flatDiagnostics };
}

// TODO: remove when our testers are using the new structure
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
  return preprocessDiagnostics(flattened);
}

function preprocessDiagnostics(flatDiagnostics) {
  flatDiagnostics.forEach(entry => {
    for (const [key, data] of Object.entries(entry)) {
      // TODO: endpoint probably shouldn't send db keys in the first place
      if(data === null || data === "" || ['createdAt', 'updatedAt', 'canteenId'].indexOf(key) !== -1) {
        delete entry[key];
      } else if(key === 'year') {
        // year expected to be number everywhere
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
  diagnostics = preprocessDiagnostics(diagnostics);
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
      localStorage.removeItem(LOCAL_FLAT_KEY);
      // TODO: remove when our testers are using the new structure
      localStorage.removeItem('diagnostics');
    }
  }

  if(!isSaved) {
    localStorage.setItem(LOCAL_FLAT_KEY, JSON.stringify(diagnostics));
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
