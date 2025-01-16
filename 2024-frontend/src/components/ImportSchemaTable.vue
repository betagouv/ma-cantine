<script setup>
import { shallowRef } from "vue"
import schemaService from "@/services/schemas.js"
import ImportSchemaTableDescriptionCell from "@/components/ImportSchemaTableDescriptionCell.vue"

/* Data */
const props = defineProps(["url"])
const headers = ["Nom de colonne", "Description", "Format", "Exemple", "Obligatoire"]
const rows = shallowRef([])

/* Fields */
schemaService.getFields(props.url).then((fields) => {
  rows.value = formatFields(fields)
})

const formatFields = (fields) => {
  const rows = []
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
    rows.push(row)
  })
  return rows
}
</script>

<template>
  <DsfrTable class="ma-cantine--table-sticky-head ma-cantine--table-white" :headers="headers" :rows="rows" />
</template>
