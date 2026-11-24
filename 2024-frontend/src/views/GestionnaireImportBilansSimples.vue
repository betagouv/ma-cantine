<script setup>
import documentation from "@/data/documentation.json"
import LayoutImport from "@/layouts/LayoutImport.vue"

/* Data */
const schemaFile = "bilans_simple_id_2026.json"
const exampleFile = {
  name: "importer_des_bilans_simples_id_2026_exemple.xlsx",
  size: "7 ko",
}
const filePreviews = {
  success: "importer_des_bilans_simples_id_2026_exemple_fichier_accepte.jpg?v=2",
  altSuccess: "Exemple de fichier accepté pour importer des bilans simples avec identification de la cantine via son ID, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "importer_des_bilans_simples_id_2026_exemple_fichier_rejete.jpg?v=2",
  altError: "Exemple de fichier rejeté pour importer des bilans simples avec identification de la cantine via son ID, qui contient des erreurs dans les colonnes ou les valeurs",
}
const links = [
  {
    title: "Où trouver l'ID de ma cantine ou de mon groupe ?",
    href: documentation.trouverIdCantine,
  }
]

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
    :links
    apiUrl="importDiagnostics/simple"
    apiImportType="id"
    schemaVersion="2026"
    :successMessage
  >
    Notre outil d'import de masse vous permet d'ajouter les bilans simplifiés de toutes vos cantines d'un coup.
  </LayoutImport>
</template>
