<script setup>
import { shallowRef } from "vue"
import schemaService from "@/services/schemas.js"
import ImportSchemaTableDescriptionCell from "@/components/ImportSchemaTableDescriptionCell.vue"

/* Table props */
const headers = ["Nom de colonne", "Description", "Format", "Exemple", "Obligatoire"]
const rows = shallowRef([])

/* Schema data */
const props = defineProps(["url"])
const schemaTypes = {
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
schemaService.getFields(props.url).then((fields) => {
  rows.value = formatFieldsForRows(fields)
})

/* Format fields to match rows expected content */
const formatFieldsForRows = (fields) => {
  const cleanedFields = []
  fields.forEach((field) => {
    const row = [
      field.name,
      {
        component: ImportSchemaTableDescriptionCell,
        title: field.title,
        description: field.description,
        constraints: field.constraints.enum,
        multiple: field.constraints.enum_multiple,
        separator: field.constraints.enum_multiple_seperator,
      },
      getType(field),
      field.example,
      field.constraints && field.constraints.required ? "Oui" : "Non",
    ]
    cleanedFields.push(row)
  })
  return cleanedFields
}

/* Clean cells content */
const getType = (field) => {
  if (field.name in schemaTypes) {
    return schemaTypes[field.name]
  }
  if (field.constraints && field.constraints.enum) {
    if (field.constraints.enum_multiple) {
      return schemaTypes[`${field.type}_enum_multiple`]
    }
    return schemaTypes[`${field.type}_enum`]
  }
  return schemaTypes[field.type]
}
</script>

<template>
  <DsfrTable class="import-schema-table" :headers="headers" :rows="rows" />
</template>

<style lang="scss">
.import-schema-table {
  white-space: nowrap;

  th {
    white-space: nowrap;
  }

  td:first-child {
    font-weight: 700;
  }

  td:last-child {
    text-align: center;
  }

  td:nth-child(2),
  th:nth-child(2) {
    white-space: wrap;
    width: 100%;
  }
}
</style>
