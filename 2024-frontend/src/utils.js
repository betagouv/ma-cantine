// this function takes vuelidate error messages and concatenates them
export const formatError = (data) => {
  return data.$errors.map((e) => e.$message).join(" ")
}

export const formatNumber = (value) => {
  if (value || value === 0) {
    const formatter = new Intl.NumberFormat("fr-FR")
    return formatter.format(value)
  }
  return "—"
}

const strictIsNaN = (x) => {
  return Number(x) !== x
}

const toPercentage = (value, round = true) => {
  if (!value && value !== 0) return null
  return round ? Math.round(value * 100) : value * 100
}

export const getSum = (values) => {
  return values.reduce((acc, value) => {
    return acc + (value || 0)
  }, 0)
}

export const getPercentage = (partialValue, totalValue, round = true) => {
  if (strictIsNaN(partialValue) || strictIsNaN(totalValue) || totalValue === 0) {
    return null
  } else {
    return toPercentage(partialValue / totalValue, round)
  }
}

// Reads a File into a base64 data URL (compatible with DRF's Base64FileField).
export const toBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = (error) => reject(error)
  })
}

// Formats ISO 8601 date strings (not datetime). Expects YYYY-MM-DD format.
export const formatDate = (
  dateString,
  options = {
    year: "numeric",
    month: "short",
    day: "numeric",
  }
) => {
  const dateSegments = dateString.split("-")
  const date = new Date(parseInt(dateSegments[0]), parseInt(dateSegments[1]) - 1, parseInt(dateSegments[2]))
  return date.toLocaleString("fr", options)
}


// Format SIRET or SIREN number
export const formatSiretOrSiren = (number) => {
  if (number == null || number === '') return number
  const digits = String(number).replace(/\s/g, '')
  const formatted = digits.slice(0, 9).replace(/(\d{3})(?=\d)/g, '$1 ')
  const rest = digits.slice(9)
  return rest ? `${formatted} ${rest}` : formatted
}
