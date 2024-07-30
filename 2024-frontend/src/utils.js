// this function takes vuelidate error messages and concatenates them
export const formatError = (data) => {
  return data.$errors.map((e) => e.$message).join(" ")
}
