const getFields = async (url) => {
  return await fetch(url)
    .then((response) => response.json())
    .then((json) => json.fields)
}

const getFieldType = (field) => {
  const types = {
    date: "Date (au format AAAA-MM-JJ)",
    integer: "Chiffre",
    number: "Chiffre",
    siret: "14 chiffres (avec ou sans espaces)",
    siret_livreur_repas: "14 chiffres (avec ou sans espaces)",
    string: "Texte (libre)",
    string_enum: "Texte (choix unique)",
    string_enum_multiple: "Texte (choix multiples)",
    year: "Année (AAAA)",
  }

  if (field.constraints) {
    if (field.constraints.enum) {
      return types[`${field.type}_enum`]
    } else if (field.constraints.pattern && field.doc_enum_multiple) {
      return types[`${field.type}_enum_multiple`]
    }
  }
  return types[field.type]
}

export default { getFields, getFieldType }
