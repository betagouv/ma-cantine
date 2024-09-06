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

export const getPercentage = (partialValue, totalValue, round = true) => {
  if (strictIsNaN(partialValue) || strictIsNaN(totalValue) || totalValue === 0) {
    return null
  } else {
    return toPercentage(partialValue / totalValue, round)
  }
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
