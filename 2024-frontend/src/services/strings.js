const onlyAlphaNumericChars = (string) => {
  // TODO à améliorer et compléter
  return string
    .toLowerCase()
    .replaceAll("-", " ")
    .replaceAll("'", " ")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
}

const checkIfStartsWith = (string, search) => {
  const cleanString = onlyAlphaNumericChars(string)
  const cleanSearch = onlyAlphaNumericChars(search)
  return cleanString.startsWith(cleanSearch)
}

const checkIfContains = (string, search) => {
  const cleanString = onlyAlphaNumericChars(string)
  const cleanSearch = onlyAlphaNumericChars(search)
  return cleanString.indexOf(cleanSearch) >= 0
}

export default { onlyAlphaNumericChars, checkIfStartsWith, checkIfContains }
