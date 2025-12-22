<script setup>
import { shallowRef } from "vue"
import schemaService from "@/services/schemas.js"
import ImportSchemaTableDescriptionCell from "@/components/ImportSchemaTableDescriptionCell.vue"

/* Data */
const props = defineProps(["schemaFile"])
const headers = ["Ordre", "Colonne", "Description", "Format", "Exemple", "Obligatoire"]
const rows = shallowRef([])

/* Fields */
schemaService.getFields(props.schemaFile).then((fields) => {
  rows.value = formatFields(fields)
})

const indexToLetter = (index) => {
  return String.fromCharCode(65 + index) // 65 is the ASCII code for 'A'
}

const formatFields = (fields) => {
  const rows = []
  fields.forEach((field, idx) => {
    const row = [
      indexToLetter(idx),
      field.name,
      {
        component: ImportSchemaTableDescriptionCell,
        id: field.name,
        title: field.title,
        description: field.description,
        constraints: field?.constraints?.enum || field?.doc_enum,
        multiple: field.doc_enum_multiple,
        separator: field.doc_enum_multiple_seperator,
      },
      schemaService.getFieldType(field),
      field.example,
      field.constraints && field.constraints.required ? "Oui" : "Non",
    ]
    rows.push(row)
  })
  return rows
}
</script>

<template>
  <DsfrTable
    class="ma-cantine--table-sticky-head ma-cantine--table-white import-schema-table"
    :headers="headers"
    :rows="rows"
  />
</template>

<style lang="scss">
.import-schema-table {
  tr {
    &:has(.admin) {
      background-color: var(--background-alt-blue-france) !important;
      td:first-child,
      td:nth-child(2) {
        color: var(--text-title-blue-france) !important;
      }
    }
    &:has(.selected) {
      background-color: var(--background-alt-red-marianne) !important;
      td:first-child,
      td:nth-child(2) {
        color: var(--text-title-red-marianne) !important;
      }
    }
    td:nth-child(2) {
      font-weight: bold;
    }
  }
}
</style>
