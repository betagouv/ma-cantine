// this function takes vuelidate error messages and concatenates them
export const formatError = (data) => {
  return data.$errors.map((e) => e.$message).join(" ")
}

export const formatNoValue = (value) => {
  if (value || value === 0) return value
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
