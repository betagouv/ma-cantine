import Constants from "@/constants"
import jsonDepartments from "@/departments.json"
import jsonRegions from "@/regions.json"

export const timeAgo = (date, displayPrefix = false) => {
  if (typeof date === "string") {
    date = new Date(date)
  }

  let prefix = ""
  if (displayPrefix) {
    prefix = "il y a "
  }

  const seconds = (new Date() - date) / 1000
  if (seconds < 60) {
    return "à l'instant"
  }
  const minutes = Math.round(seconds / 60)
  if (minutes < 60) {
    return `${prefix}${minutes} m`
  }
  const hours = Math.round(seconds / 3600)
  if (hours < 24) {
    return `${prefix}${hours} h`
  }
  const days = Math.round(seconds / 3600 / 24)
  if (days < 7) {
    return `${prefix}${days} j`
  }

  prefix = "le "

  if (days < 120) {
    return prefix + date.toLocaleString("fr-FR", { month: "long", day: "numeric" })
  }
  return prefix + date.toLocaleString("fr-FR", { month: "long", day: "numeric", year: "numeric" })
}
export const toBase64 = (file, success, error) => {
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = function() {
    success(reader.result)
  }
  if (error) reader.onerror = error
}

const arraysMatch = (arr1, arr2) => {
  if (arr1.length !== arr2.length) return false

  function compare(item1, item2) {
    var type1 = Object.prototype.toString.call(item1)
    var type2 = Object.prototype.toString.call(item2)

    // If items are different types
    if (type1 !== type2) return false

    // If an object, compare
    if (type1 === "[object Object]") return Object.keys(getObjectDiff(item1, item2)).length === 0

    // If an array, compare
    if (type1 === "[object Array]") return arraysMatch(item1, item2)

    // If it's a function, convert to a string and compare
    if (type1 === "[object Function]") return item1.toString() === item2.toString()

    return item1 === item2
  }

  for (var i = 0; i < arr1.length; i++) {
    if (!compare(arr1[i], arr2[i])) return false
  }

  return true
}

export const getObjectDiff = (obj1, obj2, keysToIgnore) => {
  if (!obj2 || Object.prototype.toString.call(obj2) !== "[object Object]") {
    return obj1
  }

  let diffs = {}
  let key

  let compare = function(item1, item2, key) {
    var type1 = Object.prototype.toString.call(item1)
    var type2 = Object.prototype.toString.call(item2)

    // If type2 is undefined it has been removed
    if (type2 === "[object Undefined]") {
      diffs[key] = null
      return
    }

    // If items are different types
    if (type1 !== type2) {
      diffs[key] = item2
      return
    }

    // If an object, compare recursively
    if (type1 === "[object Object]") {
      var objDiff = getObjectDiff(item1, item2)
      if (Object.keys(objDiff).length > 0) {
        diffs[key] = objDiff
      }
      return
    }

    // If an array, compare
    if (type1 === "[object Array]") {
      if (!arraysMatch(item1, item2)) {
        diffs[key] = item2
      }
      return
    }

    // If it's a function, convert to a string and compare
    if (type1 === "[object Function]") {
      if (item1.toString() !== item2.toString()) {
        diffs[key] = item2
      }
    } else {
      if (item1 !== item2) {
        diffs[key] = item2
      }
    }
  }

  keysToIgnore = keysToIgnore || []
  for (key in obj1) {
    if (keysToIgnore.indexOf(key) === -1) {
      if (Object.prototype.hasOwnProperty.call(obj1, key)) {
        compare(obj1[key], obj2[key], key)
      }
    }
  }

  for (key in obj2) {
    if (keysToIgnore.indexOf(key) === -1) {
      if (Object.prototype.hasOwnProperty.call(obj2, key)) {
        if (!obj1[key] && obj1[key] !== obj2[key]) {
          diffs[key] = obj2[key]
        }
      }
    }
  }

  return diffs
}

export const strictIsNaN = (x) => {
  return Number(x) !== x
}

// For graphs, badges and calculations, we only need one of the
// values of the appro - meaning the fields on fish/meat
// needed for the loi Climat are not necessary
export const hasDiagnosticApproData = (diagnostic) => {
  const approSimplifiedFields = [
    "valueBioHt",
    "valueSustainableHt",
    "valueExternalityPerformanceHt",
    "valueEgalimOthersHt",
  ]
  const characteristicGroups = Constants.TeledeclarationCharacteristicGroups
  const approExtendedFields = characteristicGroups.egalim.fields
    .concat(characteristicGroups.outsideLaw.fields)
    .concat(characteristicGroups.nonEgalim.fields)
  const hasTotal =
    diagnostic.valueTotalHt > 0 ||
    diagnostic.valueTotalHt === 0 ||
    diagnostic.percentageValueTotalHt > 0 ||
    diagnostic.percentageValueTotalHt === 0
  const approFields = diagnostic.diagnosticType === "COMPLETE" ? approExtendedFields : approSimplifiedFields
  const percentageApproFields = approFields.map((x) => `percentage${x.charAt(0).toUpperCase() + x.slice(1)}`)
  return (
    hasTotal &&
    approFields.concat(percentageApproFields).some(
      // sadly null >= 0 is true
      (key) => diagnostic[key] > 0 || diagnostic[key] === 0
    )
  )
}

export const lastYear = () => new Date().getFullYear() - 1

export const diagnosticYears = () => {
  const thisYear = new Date().getFullYear()
  return [thisYear - 1, thisYear]
}

export const customDiagnosticYears = (diagnostics) => {
  const years = diagnostics.map((d) => +d.year)
  const thisYear = new Date().getFullYear()
  const lastYear = thisYear - 1
  if (years.indexOf(thisYear) === -1) years.push(thisYear)
  if (years.indexOf(lastYear) === -1) years.push(lastYear)
  years.sort((a, b) => a - b)
  return years
}

export const diagnosticsMap = (diagnostics) => {
  const diagnosticsWithDefault = diagnosticYears().map(
    (year) => diagnostics.find((x) => x.year === year) || Object.assign({}, Constants.DefaultDiagnostics, { year })
  )
  return {
    previous: diagnosticsWithDefault[0],
    latest: diagnosticsWithDefault[1],
  }
}

export const latestCreatedDiagnostic = (diagnostics) => {
  const minYear = 2016
  const maxYear = lastYear()
  let diagnostic = undefined
  for (let year = maxYear; year >= minYear; year--) {
    diagnostic = diagnostics.find((d) => d.year === year)
    if (diagnostic) break
  }
  return diagnostic
}

export const toPercentage = (value, round = true) => {
  if (!value) return null
  return round ? Math.round(value * 100) : value * 100
}

export const getPercentage = (partialValue, totalValue, round = true) => {
  if (strictIsNaN(partialValue) || strictIsNaN(totalValue) || totalValue === 0) {
    return null
  } else {
    return toPercentage(partialValue / totalValue, round)
  }
}

// Currently we check for the existence of the key, where we mean to verify whether
// the value is null or not. If we wanted to make this change, we would also need to
// modify line 33 of api/serializers/utils.py to ensure all values are added regardless
// of their nullability
export const hasApproGraphData = (diagnostic) => {
  const graphDataKeys = [
    "percentageValueBioHt",
    "percentageValueSustainableHt",
    "percentageValueExternalityPerformanceHt",
    "percentageValueEgalimOthersHt",
  ]
  return graphDataKeys.some((k) => Object.hasOwn(diagnostic, k))
}

export const getSustainableTotal = (diagnostic) => {
  const sustainableSum =
    (diagnostic.valueSustainableHt || 0) +
    (diagnostic.valueExternalityPerformanceHt || 0) +
    (diagnostic.valueEgalimOthersHt || 0) +
    (diagnostic.percentageValueSustainableHt || 0) +
    (diagnostic.percentageValueExternalityPerformanceHt || 0) +
    (diagnostic.percentageValueEgalimOthersHt || 0)
  return sustainableSum
}

// returns a dict of integers (null/0-100) for the appro %
export const getApproPercentages = (diagnostic) => {
  // two cases: 1) raw data in diagnostic; 2) only percentages in diagnostic
  const valueTotal = diagnostic.percentageValueTotalHt || diagnostic.valueTotalHt
  const valueBio = diagnostic.percentageValueBioHt || diagnostic.valueBioHt
  const valueMeatPoultryTotal = diagnostic.valueMeatPoultryHt || 1
  const valueMeatPoultryEgalim = diagnostic.percentageValueMeatPoultryEgalimHt || diagnostic.valueMeatPoultryEgalimHt
  const valueMeatPoultryFrance = diagnostic.percentageValueMeatPoultryFranceHt || diagnostic.valueMeatPoultryFranceHt
  const valueFishTotal = diagnostic.valueFishHt || 1
  const valueFishEgalim = diagnostic.percentageValueFishEgalimHt || diagnostic.valueFishEgalimHt

  const allSustainable = getSustainableTotal(diagnostic)
  const allEgalim = (valueBio || 0) + (allSustainable || 0)
  return {
    bio: getPercentage(valueBio, valueTotal),
    allSustainable: getPercentage(allSustainable, valueTotal),
    egalim: getPercentage(allEgalim, valueTotal),
    meatPoultryEgalim: getPercentage(valueMeatPoultryEgalim, valueMeatPoultryTotal),
    meatPoultryFrance: getPercentage(valueMeatPoultryFrance, valueMeatPoultryTotal),
    fishEgalim: getPercentage(valueFishEgalim, valueFishTotal),
  }
}

// normalise "À fîrst" to "A FIRST"
export const normaliseText = (name) => {
  return name
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toUpperCase()
}

export const applicableDiagnosticRules = (canteen, year) => {
  let bioThreshold = 20
  let qualityThreshold = 50
  let hasQualityException = false
  if (canteen) {
    // group1 : guadeloupe, martinique, guyane, la_reunion, saint_martin
    const group1 = ["01", "02", "03", "04"]
    const saintMartin = "978"
    hasQualityException = true
    if (group1.indexOf(canteen.region) > -1 || canteen.department === saintMartin) {
      bioThreshold = 5
      qualityThreshold = 20
    } else if (canteen.region === "06") {
      // group2 : mayotte
      bioThreshold = 2
      qualityThreshold = 5
    } else if (canteen.department === "975") {
      // group3 : saint_pierre_et_miquelon
      bioThreshold = 10
      qualityThreshold = 30
    } else {
      hasQualityException = false
    }
  }
  // extra questions should correspond to the rules in teledeclaration view : _get_applicable_diagnostic_rules
  const shouldHaveDailyMealCount = canteen && canteen.productionType !== "central"
  return {
    hasDonationAgreement: shouldHaveDailyMealCount ? canteen.dailyMealCount >= 3000 : true,
    hasDiversificationPlan: shouldHaveDailyMealCount ? canteen.dailyMealCount >= 200 : true,
    bioThreshold,
    qualityThreshold,
    hasQualityException,
    regionForQualityException: hasQualityException && canteen.region,
    meatPoultryEgalimThreshold: year >= 2024 ? 60 : null,
    meatPoultryFranceThreshold: year >= 2024 ? 60 : null,
    fishEgalimThreshold: year >= 2024 ? 60 : null,
  }
}

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error#custom_error_types
export class AuthenticationError extends Error {
  constructor(...params) {
    super(...params)
    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AuthenticationError)
    }
    this.name = "AuthenticationError"
  }
}

export class BadRequestError extends Error {
  constructor(jsonPromise, ...params) {
    super(...params)
    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, BadRequestError)
    }
    this.name = "BadRequestError"
    this.jsonPromise = jsonPromise
  }
}

// Formats ISO 8601 date strings (not datetime). Expects YYYY-MM-DD format.
export const formatDate = (dateString) => {
  const options = {
    year: "numeric",
    month: "short",
    day: "numeric",
  }
  const dateSegments = dateString.split("-")
  const date = new Date(parseInt(dateSegments[0]), parseInt(dateSegments[1]) - 1, parseInt(dateSegments[2]))
  return date.toLocaleString("fr", options)
}

export const sectorsSelectList = (sectors, category = null) => {
  sectors = JSON.parse(JSON.stringify(sectors))
  if (category) {
    sectors = sectors.filter((s) => s.category === category)
  }
  const categories = sectors.map((s) => s.category)
  // unique filter : https://stackoverflow.com/a/14438954/3845770
  const uniqueCategories = categories.filter((c, idx, self) => c && self.indexOf(c) === idx)
  const categoryDisplay = Constants.SectorCategoryTranslations
  uniqueCategories.forEach((c) => sectors.push({ header: categoryDisplay[c], category: c }))
  const categoryOrder = [
    "administration",
    "education",
    "health",
    "social",
    "leisure",
    "enterprise",
    "autres",
    "inconnu",
  ]
  sectors.forEach((s) => (s.sortCategoryValue = s.category ? categoryOrder.indexOf(s.category) : -1))

  // Need to specify every case because browsers handle them differently
  let sortFn = (key) => {
    return (a, b) => {
      if (!a[key] && !b[key]) return 0
      if (a[key] && !b[key]) return 1
      if (b[key] && !a[key]) return -1
      if (a[key] == b[key]) return 0
      // push any 'other' sector to the bottom of their category
      if (typeof a[key] === "string" && typeof b[key] === "string") {
        const aIsOther = a[key].toLowerCase().startsWith("autre")
        const bIsOther = b[key].toLowerCase().startsWith("autre")
        if (aIsOther && !bIsOther) return 1
        else if (bIsOther && !aIsOther) return -1
        // otherwise let it be sorted below
      }
      return a[key] > b[key] ? 1 : -1
    }
  }

  sectors.sort(sortFn("name")) // added benefit of getting the headers to the top of the lists
  sectors.sort(sortFn("sortCategoryValue")) // added benefit of moving sectors without parent to top
  return sectors
}

export const sectorDisplayString = (canteenSectors, sectors) => {
  if (!canteenSectors) return ""
  const sectorDisplay = canteenSectors
    .map((sectorId) => sectors.find((x) => x.id === sectorId).name.toLowerCase())
    .join(", ")
  return capitalise(sectorDisplay)
}

export const readCookie = (name) => {
  const nameEQ = name + "="
  const cookieArr = document.cookie.split(";")
  for (let i = 0; i < cookieArr.length; i++) {
    var cookie = cookieArr[i].trimStart()
    if (cookie.indexOf(nameEQ) == 0) return cookie.substring(nameEQ.length, cookie.length)
  }
  return null
}

export const largestId = (objects) => {
  return Math.max(...objects.map((x) => x.id))
}

export const bannerCookieName = "lastHiddenCommunityEventId"

export const hideCommunityEventsBanner = (events, store) => {
  if (events.length === 0) return
  const expirationDate = new Date()
  expirationDate.setFullYear(expirationDate.getFullYear() + 1)
  const lastEventId = largestId(events)
  document.cookie = `${bannerCookieName}=${lastEventId};max-age=31536000;path=/;expires=${expirationDate.toUTCString()};SameSite=Strict;`
  store.dispatch("setShowWebinaireBanner", false)
}

export const capitalise = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

export const toCurrency = (value) => {
  if (typeof value !== "number") {
    return value
  }
  const formatter = new Intl.NumberFormat("fr-FR", {
    style: "currency",
    currency: "EUR",
  })
  return formatter.format(value)
}

export const approTotals = (diagnostic) => {
  let bioTotal = diagnostic.valueBioHt
  let siqoTotal = diagnostic.valueSustainableHt
  let perfExtTotal = diagnostic.valueExternalityPerformanceHt
  let egalimOthersTotal = diagnostic.valueEgalimOthersHt
  const usesExtendedDiagnostic = diagnostic.diagnosticType === "COMPLETE"
  if (usesExtendedDiagnostic) {
    bioTotal = 0
    siqoTotal = 0
    perfExtTotal = 0
    egalimOthersTotal = 0
    const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields
    egalimFields.forEach((field) => {
      const value = parseFloat(diagnostic[field])
      if (value) {
        if (field.endsWith("Bio")) {
          bioTotal += value
        } else if (!field.startsWith("valueLabel") && !field.endsWith("Ht")) {
          if (field.endsWith("LabelRouge") || field.endsWith("AocaopIgpStg")) {
            siqoTotal += value
          } else if (field.endsWith("Performance") || field.endsWith("Externalites")) {
            perfExtTotal += value
          } else {
            egalimOthersTotal += value
          }
        }
      }
    })
    bioTotal = +bioTotal.toFixed(2)
    siqoTotal = +siqoTotal.toFixed(2)
    perfExtTotal = +perfExtTotal.toFixed(2)
    egalimOthersTotal = +egalimOthersTotal.toFixed(2)
  }
  return {
    bioTotal,
    siqoTotal,
    perfExtTotal,
    egalimOthersTotal,
  }
}

export const approSummary = (diagnostic) => {
  if (diagnostic.valueTotalHt > 0) {
    const { bioTotal, siqoTotal, perfExtTotal, egalimOthersTotal } = approTotals(diagnostic)
    let qualityTotal
    if (siqoTotal || perfExtTotal || egalimOthersTotal) {
      qualityTotal = (siqoTotal || 0) + (perfExtTotal || 0) + (egalimOthersTotal || 0)
    }
    let summary = []
    if (hasValue(bioTotal)) {
      summary.push(`${getPercentage(bioTotal, diagnostic.valueTotalHt)} % bio`)
    }
    if (hasValue(qualityTotal)) {
      summary.push(`${getPercentage(qualityTotal, diagnostic.valueTotalHt)} % de qualité et durable`)
    }
    return summary.join(", ")
  }
  return "Incomplet"
}

export const departmentItems = jsonDepartments.map((x) => ({
  text: `${x.departmentCode} - ${x.departmentName}`,
  value: x.departmentCode,
}))

export const selectListToObject = (selectList) => {
  return selectList.reduce((acc, val) => {
    acc[val.value] = val.label
    return acc
  }, {})
}

function hasValue(val) {
  if (typeof val === "string") {
    return !!val
  } else {
    return !strictIsNaN(val)
  }
}

export const hasStartedMeasureTunnel = (diagnostic, keyMeasure) => {
  if (diagnostic?.creationSource === "TUNNEL") return !!diagnostic[keyMeasure.progressField]
  return !!diagnostic
}

export const hasFinishedMeasureTunnel = (diagnostic) => {
  if (diagnostic?.creationSource === "TUNNEL") {
    const measureProgressFields = ["tunnelAppro", "tunnelWaste", "tunnelDiversification", "tunnelPlastic", "tunnelInfo"]
    return measureProgressFields.every((field) => diagnostic[field] === "complet")
  }
  return !!diagnostic
}

export const getCharacteristicFromFieldSuffix = (fieldSuffix, tdGroup) => {
  const normalisedGroupCharacteristics = tdGroup.characteristics.map((g) => g.toLowerCase().replace(/_/g, ""))
  const fieldCharacteristic = fieldSuffix.toLowerCase()
  const charIdx = normalisedGroupCharacteristics.indexOf(fieldCharacteristic)
  if (charIdx === -1) return fieldSuffix
  const originalChar = tdGroup.characteristics[charIdx]
  return Constants.TeledeclarationCharacteristics[originalChar]
}

export const getCharacteristicFromField = (fieldName, fieldPrefix, tdGroup) => {
  const fieldSuffix = fieldName.split(fieldPrefix)[1]
  return getCharacteristicFromFieldSuffix(fieldSuffix, tdGroup)
}

export const hasSatelliteInconsistency = (canteen) => {
  if (!canteen || !canteen.isCentralCuisine) return false
  if (!canteen.satelliteCanteensCount) return true
  if (!canteen.satellites) return true
  return canteen.satelliteCanteensCount !== canteen.satellites.length
}

export const lineMinistryRequired = (canteen, allSectors) => {
  const concernedSectors = allSectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
  if (concernedSectors.length === 0) return false
  return canteen.sectors.some((x) => concernedSectors.indexOf(x) > -1)
}

export const missingCanteenData = (canteen, sectors) => {
  // TODO: what location data to we require at minimum?
  const requiredFields = ["siret", "name", "cityInseeCode", "productionType", "managementType"]
  const missingFieldLambda = (f) => !canteen[f]
  const missingSharedRequiredData = requiredFields.some(missingFieldLambda)
  if (missingSharedRequiredData) return true

  // sectors checks
  if (!canteen.sectors || !canteen.sectors.length) return true
  if (lineMinistryRequired(canteen, sectors) && !canteen.lineMinistry) return true

  // production type specific checks
  const yearlyMealCountKey = "yearlyMealCount"
  const onSiteFields = ["dailyMealCount", yearlyMealCountKey]
  const centralKitchenFields = [yearlyMealCountKey, "satelliteCanteensCount"]
  const satelliteFields = ["centralProducerSiret"]

  if (canteen.productionType === "central") {
    return centralKitchenFields.some(missingFieldLambda)
  } else if (canteen.productionType === "central_serving") {
    return centralKitchenFields.some(missingFieldLambda) && onSiteFields.some(missingFieldLambda)
  } else if (canteen.productionType === "site_cooked_elsewhere") {
    return onSiteFields.some(missingFieldLambda) && satelliteFields.some(missingFieldLambda)
  } else if (canteen.productionType === "site") {
    return onSiteFields.some(missingFieldLambda)
  }
  return true // shouldn't get to here, indicates a bug in our logic/data
}

export const inTeledeclarationCampaign = (year) => {
  const tdYear = lastYear()
  const inTdCampaign = window.ENABLE_TELEDECLARATION && year === tdYear
  return inTdCampaign
}

export const diagnosticCanBeTeledeclared = (canteen, diagnostic) => {
  if (!canteen || !diagnostic) return false

  if (!inTeledeclarationCampaign(diagnostic.year)) return false

  const hasActiveTeledeclaration = diagnostic.teledeclaration?.status === "SUBMITTED"
  if (hasActiveTeledeclaration) return false

  if (canteen.productionType === "site_cooked_elsewhere") {
    const tdYear = lastYear()
    const ccDiag = canteen.centralKitchenDiagnostics?.find((x) => x.year === tdYear)
    if (ccDiag) {
      const noNeedToTd = ccDiag.centralKitchenDiagnosticMode === "ALL"
      const canSubmitOtherData = !noNeedToTd
      const hasOtherData = !!diagnostic
      return canSubmitOtherData && hasOtherData
    }
    // satellites can still TD if CCs haven't
  }

  return hasDiagnosticApproData(diagnostic)
}

export const readyToTeledeclare = (canteen, diagnostic, sectors) => {
  return (
    diagnosticCanBeTeledeclared(canteen, diagnostic) &&
    !hasSatelliteInconsistency(canteen) &&
    !missingCanteenData(canteen, sectors)
  )
}

// for diagnostics created before the redesign launched in 2024, many null values
// were interpreted as false. Since then, we ask for an explicit false value.
export const diagnosticUsesNullAsFalse = (diagnostic) => {
  return diagnostic.year < 2023
}

export const regionDisplayName = (regionCode) => {
  return jsonRegions.find((r) => r.regionCode === regionCode).regionName
}
