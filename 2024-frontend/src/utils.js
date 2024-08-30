// this function takes vuelidate error messages and concatenates them
export const formatError = (data) => {
  return data.$errors.map((e) => e.$message).join(" ")
}

export const formatNoValue = (value) => {
  if (value || value === 0) return value
  return "—"
}
