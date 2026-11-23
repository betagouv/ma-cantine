<script setup>
import LayoutImport from "@/layouts/LayoutImport.vue"

/* Data */
const schemaFile = "cantines_gestionnaires.json"

/* Success */
const successMessage = (count) => count > 1
  ? "Vos cantines sont modifiées."
  : "Votre cantine est modifiée."
</script>

<template>
  <LayoutImport
    :schemaFile
    adminCallout
    apiUrl="importCanteensManagers"
    :successMessage
  />
</template>
