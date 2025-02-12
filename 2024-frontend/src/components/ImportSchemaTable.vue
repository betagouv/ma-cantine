<script setup>
import { shallowRef } from "vue"
import schemaService from "@/services/schemas.js"
import ImportSchemaTableDescriptionCell from "@/components/ImportSchemaTableDescriptionCell.vue"

/* Data */
const props = defineProps(["schemaFile"])
const headers = ["Nom de colonne", "Description", "Format", "Exemple", "Obligatoire"]
const rows = shallowRef([])

/* Fields */
schemaService.getFields(props.schemaFile).then((fields) => {
  rows.value = formatFields(fields)
})

const formatFields = (fields) => {
  const rows = []
  fields.forEach((field) => {
    const row = [
      field.name,
      {
        component: ImportSchemaTableDescriptionCell,
        id: field.name,
        title: field.title,
        description: field.description,
        constraints: field.constraints.enum || field.doc_enum,
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
  <DsfrTable class="ma-cantine--table-sticky-head ma-cantine--table-white" :headers="headers" :rows="rows" />
</template>
