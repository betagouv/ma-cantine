<script setup>
import documentation from "@/data/documentation.json"
import LayoutImport from "@/layouts/LayoutImport.vue"
import ImportDeprecatedWarning from "@/components/ImportDeprecatedWarning.vue"

/* Data */
const schemaFile = "bilans_detaille_siret.json"
const exampleFile = {
  name: "importer_des_bilans_detailles_exemple.xlsx",
  size: "9 ko",
}
const links = [
  {
    title: "Liste des champs à renseigner pour importer un bilan détaillé",
    href: documentation.importBilanDetaille,
  }
]

/* Success */
const successMessage = (count) => count > 1
  ? `Les ${count} bilans détaillés ont été importés avec succès`
  : "Le bilan détaillé a été importé avec succès"
</script>

<template>
  <LayoutImport
    :schemaFile
    :exampleFile
    :links
    apiUrl="importDiagnostics/complete"
    schemaVersion="2025"
    :successMessage
  >
    <template #before-title>
      <ImportDeprecatedWarning :isDiagnostics="true" :redirectTo="{ name: 'GestionnaireImportBilansDetaillesSIRET' }" />
    </template>
    Notre outil d’import de masse vous permet d’ajouter les bilans détaillés de toutes vos cantines d’un coup.
  </LayoutImport>
</template>
