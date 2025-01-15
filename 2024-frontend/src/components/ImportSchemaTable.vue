<script setup>
import { shallowRef } from "vue"
import schemaService from "@/services/schemas.js"
import ImportSchemaTableDescriptionCell from "@/components/ImportSchemaTableDescriptionCell.vue"

/* Table props */
const headers = ["Nom de colonne", "Description", "Format", "Exemple", "Obligatoire"]
const rows = shallowRef([])

/* Schema data */
const props = defineProps(["url"])
schemaService.getFields(props.url).then((fields) => {
  rows.value = jsonToRows(fields)
})

/* Format fields to match rows expected content */
const jsonToRows = (fields) => {
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
      schemaService.getFieldType(field),
      field.example,
      field.constraints && field.constraints.required ? "Oui" : "Non",
    ]
    cleanedFields.push(row)
  })
  return cleanedFields
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
