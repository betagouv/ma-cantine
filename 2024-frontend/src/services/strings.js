const removeSpecialChars = (string) => {
  return string
    .toLowerCase()
    .replaceAll("-", " ")
    .replaceAll("'", " ")
    .normalize("NFD") // Convert string to unicode normalize : needed for accent replacement
    .replace(/[\u0300-\u036f]/g, "") // Remove accents : all chars between unicode U+0300 to U+036F
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
