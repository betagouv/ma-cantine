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

export const isDiagnosticComplete = (diagnostic) => {
  return ["valueBioHt", "valueSustainableHt", "valueTotalHt"].every(
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

export const getPercentage = (partialValue, totalValue) => {
  if (strictIsNaN(partialValue) || strictIsNaN(totalValue) || totalValue === 0) {
    return null
  } else {
    return Math.round((100 * partialValue) / totalValue)
  }
}

export const badges = (canteen, diagnostic, sectors) => {
  let applicable = JSON.parse(JSON.stringify(jsonBadges))
  if (!diagnostic) return applicable
  const bioPercent = getPercentage(diagnostic.valueBioHt, diagnostic.valueTotalHt)
  const sustainablePercent = getPercentage(diagnostic.valueSustainableHt, diagnostic.valueTotalHt)
  if (bioPercent >= 20 && bioPercent + sustainablePercent >= 50) {
    applicable.appro.earned = true
  }
  if (
    diagnostic.hasWasteDiagnostic &&
    diagnostic.wasteActions?.length > 0 &&
    (canteen.dailyMealCount <= 3000 || diagnostic.hasDonationAgreement)
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

  // We need to rethink the way a school sector is defined. Temporarily
  // using the name.
  const schoolSector = sectors.find((x) => x.name === "Scolaire")
  if (!schoolSector) console.error("No sector `Scolaire` is present in this configuration")

  if (diagnostic.vegetarianWeeklyRecurrence === "DAILY") {
    applicable.diversification.earned = true
  } else if (schoolSector && canteen.sectors.indexOf(schoolSector.id) > -1) {
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
