import Constants from "@/constants"
import jsonBadges from "@/badges"

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
  const hasTotal = diagnostic.valueTotalHt > 0 || diagnostic.valueTotalHt === 0
  const approFields = diagnostic.diagnosticType === "COMPLETE" ? approExtendedFields : approSimplifiedFields
  return (
    hasTotal &&
    approFields.some(
      // sadly null >= 0 is true
      (key) => diagnostic[key] > 0 || diagnostic[key] === 0
    )
  )
}

// For the teledeclaration, all values - including fish/meat
// which are not used for graphs and calculations - must be
// present
export const isDiagnosticComplete = (diagnostic) => {
  const approFields = [
    "valueBioHt",
    "valueSustainableHt",
    "valueTotalHt",
    "valueExternalityPerformanceHt",
    "valueEgalimOthersHt",
    "valueMeatPoultryHt",
    "valueMeatPoultryEgalimHt",
    "valueMeatPoultryFranceHt",
    "valueFishHt",
    "valueFishEgalimHt",
  ]
  return approFields.every(
    // sadly null >= 0 is true
    (key) => diagnostic[key] > 0 || diagnostic[key] === 0
  )
}

export const lastYear = () => new Date().getFullYear() - 1

export const diagnosticYears = () => {
  const thisYear = new Date().getFullYear()
  return [thisYear - 2, thisYear - 1, thisYear, thisYear + 1]
}

export const diagnosticsMap = (diagnostics) => {
  const diagnosticsWithDefault = diagnosticYears().map(
    (year) => diagnostics.find((x) => x.year === year) || Object.assign({}, Constants.DefaultDiagnostics, { year })
  )
  return {
    previous: diagnosticsWithDefault[0],
    latest: diagnosticsWithDefault[1],
    provisionalYear1: diagnosticsWithDefault[2],
    provisionalYear2: diagnosticsWithDefault[3],
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

export const getPercentage = (partialValue, totalValue, round = true) => {
  if (strictIsNaN(partialValue) || strictIsNaN(totalValue) || totalValue === 0) {
    return null
  } else {
    return round ? Math.round((100 * partialValue) / totalValue) : (100 * partialValue) / totalValue
  }
}

export const getSustainableTotal = (diagnostic) => {
  const sustainableSum =
    (diagnostic.valueSustainableHt || 0) +
    (diagnostic.valueExternalityPerformanceHt || 0) +
    (diagnostic.valueEgalimOthersHt || 0)
  return sustainableSum
}

export const badges = (canteen, diagnostic, sectors) => {
  let applicable = JSON.parse(JSON.stringify(jsonBadges))
  if (!diagnostic) return applicable
  const bioPercent = getPercentage(diagnostic.valueBioHt, diagnostic.valueTotalHt)
  const sustainablePercent = getPercentage(getSustainableTotal(diagnostic), diagnostic.valueTotalHt)
  const applicableRules = applicableDiagnosticRules(canteen)
  if (
    bioPercent >= applicableRules.bioThreshold &&
    bioPercent + sustainablePercent >= applicableRules.qualityThreshold
  ) {
    applicable.appro.earned = true
  }
  if (
    diagnostic.hasWasteDiagnostic &&
    diagnostic.wasteActions?.length > 0 &&
    (!applicableRules.hasDonationAgreement || diagnostic.hasDonationAgreement)
  ) {
    applicable.waste.earned = true
  }
  if (
    diagnostic.cookingPlasticSubstituted &&
    diagnostic.servingPlasticSubstituted &&
    diagnostic.plasticBottlesSubstituted &&
    diagnostic.plasticTablewareSubstituted
  ) {
    applicable.plastic.earned = true
  }

  const educationSectors = sectors.filter((s) => s.category === "education").map((s) => s.id)
  const inEducation = canteen.sectors.some((s) => educationSectors.indexOf(s) > -1)
  if (diagnostic.vegetarianWeeklyRecurrence === "DAILY") {
    applicable.diversification.earned = true
  } else if (inEducation) {
    if (diagnostic.vegetarianWeeklyRecurrence === "MID" || diagnostic.vegetarianWeeklyRecurrence === "HIGH") {
      applicable.diversification.earned = true
    }
  }
  if (diagnostic.communicatesOnFoodQuality) {
    applicable.info.earned = true
  }
  return applicable
}

// normalise "À fîrst" to "A FIRST"
export const normaliseText = (name) => {
  return name
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toUpperCase()
}

export const applicableDiagnosticRules = (canteen) => {
  let bioThreshold = 20
  let qualityThreshold = 50
  let hasQualityException = false
  // group1 : guadeloupe, martinique, guyane, la_reunion, TODO saint_martin
  const group1 = ["01", "02", "03", "04"]
  if (canteen) {
    hasQualityException = true
    if (group1.indexOf(canteen.region) > -1) {
      bioThreshold = 5
      qualityThreshold = 20
    } else if (canteen.region === "06") {
      // group2 : mayotte
      bioThreshold = 2
      qualityThreshold = 5
      // TODO: group3 : saint_pierre_et_miquelon
    } else {
      hasQualityException = false
    }
  }
  return {
    hasDonationAgreement: canteen ? canteen.dailyMealCount >= 3000 : true,
    hasDiversificationPlan: canteen ? canteen.dailyMealCount >= 200 : true,
    bioThreshold,
    qualityThreshold,
    hasQualityException,
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

export const sectorsSelectList = (sectors) => {
  sectors = JSON.parse(JSON.stringify(sectors))
  const categories = sectors.map((s) => s.category)
  // unique filter : https://stackoverflow.com/a/14438954/3845770
  const uniqueCategories = categories.filter((c, idx, self) => c && self.indexOf(c) === idx)
  const categoryDisplay = {
    education: "Enseignement",
    health: "Santé",
    autres: "Autre",
    social: "Social et Médico-Social",
    administration: "Administration",
    leisure: "Loisirs",
    enterprise: "Entreprise",
  }
  uniqueCategories.forEach((c) => sectors.push({ header: categoryDisplay[c], category: c }))
  const categoryOrder = ["administration", "education", "health", "social", "leisure", "enterprise", "autres"]
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
