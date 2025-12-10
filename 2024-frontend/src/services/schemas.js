const getFields = async (schemaFile) => {
  const url = `https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/charline-l/imports--canteen-remove-english-values/data/schemas/imports/${schemaFile}`
  return await fetch(url)
    .then((response) => response.json())
    .then((json) => json.fields)
}

const getFieldType = (field) => {
  const types = {
    date: "Date (au format AAAA-MM-JJ)",
    integer: "Chiffre",
    number: "Chiffre",
    siret: "14 chiffres avec ou sans espaces",
    siret_livreur_repas: "14 chiffres avec ou sans espaces",
    string: "Texte (libre)",
    string_enum: "Texte (choix unique)",
    string_enum_multiple: "Texte (choix multiples)",
    year: "Année (AAAA)",
  }

  let fieldType = ""

  switch (true) {
    case field.name in types:
      // examples: 'siret', 'siret_livreur_repas'
      fieldType = types[field.name]
      break
    case field.constraints?.enum:
      // examples: 'secteurs', 'type_production'
      fieldType = types[`${field.type}_enum`]
      break
    case field.constraints?.pattern && field.doc_enum && !field.doc_enum_multiple:
      // examples: 'famille_produits'
      fieldType = types[`${field.type}_enum`]
      break
    case field.constraints?.pattern && field.doc_enum && field.doc_enum_multiple:
      // examples: 'caracteristiques'
      fieldType = types[`${field.type}_enum_multiple`]
      break
    case field.constaints?.pattern && field.doc_pattern:
      // examples: 'number'
      fieldType = types[field.doc_pattern]
      break
    default:
      fieldType = types[field.type]
  }

  return fieldType
}

export default { getFields, getFieldType }
