import teledeclaration from "@/data/teledeclaration.json"

const getPageFields = (pageName) => {
  return teledeclaration.pages[pageName].fields
}

const getField = (fieldName) => {
  return teledeclaration.fields[fieldName]
}

export default { getPageFields, getField }
