import teledeclaration from "@/data/teledeclaration.json"

const getField = (fieldName) => {
  return teledeclaration[fieldName]
}

const getFieldError = (fieldName, errors) => {
  const hasError = errors.find(error => error.field === fieldName)
  return hasError ? hasError.message : null
}

export default { getField, getFieldError }
