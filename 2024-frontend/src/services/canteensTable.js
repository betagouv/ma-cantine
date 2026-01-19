import urlService from "@/services/urls.js"
import diagnosticService from "@/services/diagnostics.js"
import cantines from "@/data/cantines.json"
import stringService from "@/services/strings.js"

const getNameInfos = (canteen) => {
  return {
    name: canteen.name,
    url: urlService.getCanteenUrl(canteen),
    satellitesCountSentence: canteen.productionType === "groupe" ? getSatellitesCountSentence(canteen.satellitesCount) : null,
  }
}

const getSatelliteNameInfos = (canteen) => {
  return {
    canteen: canteen.name,
    url: urlService.getCanteenUrl(canteen),
    isManagedByUser: canteen.isManagedByUser,
  }
}

const getSatellitesCountSentence = (satellitesCount) => {
  const number = satellitesCount === 0 ? "Aucun" : satellitesCount
  const name = satellitesCount <= 1 ? "restaurant satellite" : "restaurants satellites"
  return `${number} ${name}`
}

const getSiretOrSirenInfos = (canteen) => {
  return canteen.siret || canteen.sirenUniteLegale
}

const getCityInfos = (canteen) => {
  let city = ""
  if (canteen.city) city += canteen.city
  if (canteen.postalCode) city += ` (${canteen.postalCode})`
  if (!canteen.city && !canteen.postalCode) city = "Non renseigné"
  return city
}

const getProductionTypeInfos = (canteen) => {
  const slug = canteen.productionType
  const index = cantines.productionType.findIndex((type) => type.value === slug)
  return cantines.productionType[index].label
}

const getDiagnosticInfos = (canteen, campaign) => {
  const action = canteen.action
  const badge = diagnosticService.getBadge(action, campaign)
  const button = getTeledeclareButton(canteen)
  return { badge, button }
}

const getTeledeclareButton = (canteen) => {
  const button = diagnosticService.getTeledeclareButton(canteen.action)
  if (!button) return false
  const canteenUrlComponent = urlService.getCanteenUrl(canteen)
  const lastYear = new Date().getFullYear() - 1
  return { ...button, canteenUrlComponent, year: lastYear }
}

const getDailyMealCountInfos = (canteen) => {
  return canteen.dailyMealCount
}

const searchCanteensBySiretOrSirenOrName = (search, allCanteens) => {
  if (!search) return allCanteens
  const searchValue = search.trim()
  const searchWithoutSpaces = searchValue.replace(/\s/g, "")
  const filteredCanteens = allCanteens.filter((canteen) => {
    if (canteen.siret && canteen.siret.indexOf(searchWithoutSpaces) === 0) return true
    if (canteen.sirenUniteLegale && canteen.sirenUniteLegale.indexOf(searchWithoutSpaces) === 0) return true
    if (stringService.checkIfContains(canteen.name, searchValue)) return true
  })
  return filteredCanteens
}

export default {
  getNameInfos,
  getSatelliteNameInfos,
  getSiretOrSirenInfos,
  getCityInfos,
  getProductionTypeInfos,
  getDiagnosticInfos,
  getDailyMealCountInfos,
  searchCanteensBySiretOrSirenOrName,
}
