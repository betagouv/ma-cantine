import teledeclaration from "@/data/teledeclaration.json"

const getPageFields = (pageName) => {
  return teledeclaration.pages[pageName].fields
}

const getField = (fieldName) => {
  return teledeclaration.fields[fieldName]
}

const getFieldError = (fieldName, errors) => {
  const hasError = errors.find(error => error.field === fieldName)
  return hasError ? hasError.message : null
}

export default { getPageFields, getField, getFieldError }
