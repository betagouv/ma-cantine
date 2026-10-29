import teledeclaration from "@/data/teledeclaration.json"

/* Canteen fields, not teledeclaration fields */
const canteenGroups = {
  informationsCantine: ["name", "siret", "sirenUniteLegale", "postalCode", "city", "cityInseeCode", "departmentLib", "regionLib", "patListLib", "epciLib", "sectorList", "lineMinistry", "dailyMealCount", "yearlyMealCount", "economicModel", "productionType", "managementType", "centralProducerSiret", "publicationComments"],
  informationsGroupe: ["name", "sirenUniteLegale", "managementType", "dailyMealCount", "yearlyMealCount", "centralProducerSiret"],
}

/* Teledeclaration fields of the "approvisionnement" volet */
const approGroups = {
  couverts: ["nombreRepasAn"],
  saisie: ["diagnosticType"],
  valeurTotale: ["valeurTotale"],
  coutRepas: ["coutRepas"],
  egalimSimple: ["valeurTotale", "valeurBio", "valeurBioDontCommerceEquitable", "valeurSiqo", "valeurViandesVolailles", "valeurViandesVolaillesEgalim", "valeurEgalimAutres", "valeurEgalimAutresDontCommerceEquitable", "valeurExternalitesPerformance", "valeurProduitsDeLaMer", "valeurProduitsDeLaMerEgalim"],
  egalimComplete: ["valeurTotale", "valeurViandesVolailles", "valeurProduitsDeLaMer", "valeurCharcuterie", "valeurFruitsEtLegumes", "valeurProduitsLaitiers", "valeurBoulangerie", "valeurAutres", "valeurBoissons", "valeurViandesVolaillesBio", "valeurViandesVolaillesBioDontCommerceEquitable", "valeurProduitsDeLaMerBio", "valeurProduitsDeLaMerBioDontCommerceEquitable", "valeurCharcuterieBio", "valeurCharcuterieBioDontCommerceEquitable", "valeurFruitsEtLegumesBio", "valeurFruitsEtLegumesBioDontCommerceEquitable", "valeurProduitsLaitiersBio", "valeurProduitsLaitiersBioDontCommerceEquitable", "valeurBoulangerieBio", "valeurBoulangerieBioDontCommerceEquitable", "valeurAutresBio", "valeurAutresBioDontCommerceEquitable", "valeurBoissonsBio", "valeurBoissonsBioDontCommerceEquitable", "valeurViandesVolaillesLabelRouge", "valeurProduitsDeLaMerLabelRouge", "valeurCharcuterieLabelRouge", "valeurFruitsEtLegumesLabelRouge", "valeurProduitsLaitiersLabelRouge", "valeurBoulangerieLabelRouge", "valeurAutresLabelRouge", "valeurViandesVolaillesAocaop", "valeurProduitsDeLaMerAocaop", "valeurCharcuterieAocaop", "valeurFruitsEtLegumesAocaop", "valeurProduitsLaitiersAocaop", "valeurBoulangerieAocaop", "valeurAutresAocaop", "valeurBoissonsAocaop", "valeurViandesVolaillesIgp", "valeurProduitsDeLaMerIgp", "valeurCharcuterieIgp", "valeurFruitsEtLegumesIgp", "valeurProduitsLaitiersIgp", "valeurBoulangerieIgp", "valeurAutresIgp", "valeurBoissonsIgp", "valeurViandesVolaillesStg", "valeurProduitsDeLaMerStg", "valeurCharcuterieStg", "valeurFruitsEtLegumesStg", "valeurProduitsLaitiersStg", "valeurBoulangerieStg", "valeurAutresStg", "valeurBoissonsStg", "valeurViandesVolaillesHve", "valeurProduitsDeLaMerHve", "valeurCharcuterieHve", "valeurFruitsEtLegumesHve", "valeurProduitsLaitiersHve", "valeurBoulangerieHve", "valeurAutresHve", "valeurBoissonsHve", "valeurProduitsDeLaMerPecheDurable", "valeurViandesVolaillesRup", "valeurProduitsDeLaMerRup", "valeurCharcuterieRup", "valeurFruitsEtLegumesRup", "valeurProduitsLaitiersRup", "valeurBoulangerieRup", "valeurAutresRup", "valeurBoissonsRup", "valeurViandesVolaillesCommerceEquitable", "valeurProduitsDeLaMerCommerceEquitable", "valeurCharcuterieCommerceEquitable", "valeurFruitsEtLegumesCommerceEquitable", "valeurProduitsLaitiersCommerceEquitable", "valeurBoulangerieCommerceEquitable", "valeurAutresCommerceEquitable", "valeurBoissonsCommerceEquitable", "valeurViandesVolaillesFermier", "valeurProduitsDeLaMerFermier", "valeurCharcuterieFermier", "valeurFruitsEtLegumesFermier", "valeurProduitsLaitiersFermier", "valeurBoulangerieFermier", "valeurAutresFermier", "valeurBoissonsFermier", "valeurViandesVolaillesExternalites", "valeurProduitsDeLaMerExternalites", "valeurCharcuterieExternalites", "valeurFruitsEtLegumesExternalites", "valeurProduitsLaitiersExternalites", "valeurBoulangerieExternalites", "valeurAutresExternalites", "valeurBoissonsExternalites", "valeurViandesVolaillesPerformance", "valeurProduitsDeLaMerPerformance", "valeurCharcuteriePerformance", "valeurFruitsEtLegumesPerformance", "valeurProduitsLaitiersPerformance", "valeurBoulangeriePerformance", "valeurAutresPerformance", "valeurBoissonsPerformance"],
  origine: ["valeurViandesVolailles", "valeurProduitsDeLaMer", "valeurCharcuterie", "valeurFruitsEtLegumes", "valeurProduitsLaitiers", "valeurBoulangerie", "valeurAutres", "valeurBoissons", "valeurFrance", "valeurViandesVolaillesFrance", "valeurProduitsDeLaMerFrance", "valeurCharcuterieFrance", "valeurFruitsEtLegumesFrance", "valeurProduitsLaitiersFrance", "valeurBoulangerieFrance", "valeurAutresFrance", "valeurBoissonsFrance", "valeurEurope", "valeurViandesVolaillesEurope", "valeurProduitsDeLaMerEurope", "valeurCharcuterieEurope", "valeurFruitsEtLegumesEurope", "valeurProduitsLaitiersEurope", "valeurBoulangerieEurope", "valeurAutresEurope", "valeurBoissonsEurope"],
  localCircuitCourt: ["valeurCircuitCourt", "valeurViandesVolaillesCircuitCourt", "valeurProduitsDeLaMerCircuitCourt", "valeurCharcuterieCircuitCourt", "valeurFruitsEtLegumesCircuitCourt", "valeurProduitsLaitiersCircuitCourt", "valeurBoulangerieCircuitCourt", "valeurAutresCircuitCourt", "valeurBoissonsCircuitCourt", "valeurLocal", "definitionLocal", "definitionLocalKm", "valeurViandesVolaillesLocal", "valeurProduitsDeLaMerLocal", "valeurCharcuterieLocal", "valeurFruitsEtLegumesLocal", "valeurProduitsLaitiersLocal", "valeurBoulangerieLocal", "valeurAutresLocal", "valeurBoissonsLocal", "valeurViandesVolailles", "valeurProduitsDeLaMer", "valeurCharcuterie", "valeurFruitsEtLegumes", "valeurProduitsLaitiers", "valeurBoulangerie", "valeurAutres", "valeurBoissons"],
}

const groups = { ...canteenGroups, ...approGroups }

/* Fields of all the volets, the field names are unique across volets */
const fields = { ...teledeclaration.approvisionnement }

const getField = (fieldName) => {
  return fields[fieldName]
}

const getFieldError = (fieldName, errors) => {
  const hasError = errors.find(error => error.field === fieldName)
  return hasError ? hasError.message : null
}

const getFieldsListFromPage = (pageName, canteenIsGroupe, diagnosticIsSimple) => {
  switch (true) {
    case pageName === "GestionnaireTunnelApproInformations" && !canteenIsGroupe:
      return groups.informationsCantine
    case pageName === "GestionnaireTunnelApproInformations" && canteenIsGroupe:
      return groups.informationsGroupe
    case pageName === "GestionnaireTunnelApproCouverts":
      return groups.couverts
    case pageName === "GestionnaireTunnelApproSaisie":
      return groups.saisie
    case pageName === "GestionnaireTunnelApproEgalim" && diagnosticIsSimple:
      return groups.egalimSimple
    case pageName === "GestionnaireTunnelApproEgalim" && !diagnosticIsSimple:
      return groups.egalimComplete
    case pageName === "GestionnaireTunnelApproOrigine":
      return groups.origine
    case pageName === "GestionnaireTunnelApproLocalCircuitCourt":
      return groups.localCircuitCourt
    default:
      return []
  }
}

const getFieldsListFromGroup = (groupName) => {
  return groups[groupName]
}

const getFieldsWithAutofill = () => {
  return Object.keys(fields).filter((field) => fields[field].autofill)
}

export default { getField, getFieldError, getFieldsListFromPage, getFieldsListFromGroup, getFieldsWithAutofill }
