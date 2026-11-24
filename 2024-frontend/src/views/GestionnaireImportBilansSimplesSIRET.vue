<script setup>
import LayoutImport from "@/layouts/LayoutImport.vue"

/* Data */
const schemaFile = "bilans_simple_siret_2026.json"
const exampleFile = {
  name: "importer_des_bilans_simples_siret_2026_exemple.xlsx",
  size: "7 ko",
}
const filePreviews = {
  success: "importer_des_bilans_simples_siret_2026_exemple_fichier_accepte.jpg?v=2",
  altSuccess: "Exemple de fichier accepté pour importer des bilans simples, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "importer_des_bilans_simples_siret_2026_exemple_fichier_rejete.jpg?v=2",
  altError: "Exemple de fichier rejeté pour importer des bilans simples, qui contient des erreurs dans les colonnes ou les valeurs",
}

/* Success */
const successMessage = (count) => count > 1
  ? `Les ${count} bilans simples ont été importés avec succès`
  : "Le bilan simple a été importé avec succès"
</script>

<template>
  <LayoutImport
    :schemaFile
    :exampleFile
    :filePreviews
    apiUrl="importDiagnostics/simple"
    apiImportType="siret"
    schemaVersion="2026"
    :successMessage
  >
    Notre outil d'import de masse vous permet d'ajouter les bilans simplifiés de vos cantines avec numéro SIRET d'un coup.
  </LayoutImport>
</template>
