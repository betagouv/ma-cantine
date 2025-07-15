const removeSpecialChars = (string) => {
  return string
    .toLowerCase()
    .replaceAll("-", " ")
    .replaceAll("'", " ")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
}

const checkIfStartsWith = (string, search) => {
  const cleanString = removeSpecialChars(string)
  const cleanSearch = removeSpecialChars(search)
  return cleanString.startsWith(cleanSearch)
}

const checkIfContains = (string, search) => {
  const cleanString = removeSpecialChars(string)
  const cleanSearch = removeSpecialChars(search)
  return cleanString.indexOf(cleanSearch) >= 0
}

export default { removeSpecialChars, checkIfStartsWith, checkIfContains }
