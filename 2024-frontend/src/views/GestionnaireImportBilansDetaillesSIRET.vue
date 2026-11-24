<script setup>
import documentation from "@/data/documentation.json"
import LayoutImport from "@/layouts/LayoutImport.vue"

/* Data */
const schemaFile = "bilans_detaille_siret_2026.json"
const exampleFile = {
  name: "importer_des_bilans_detailles_siret_2026_exemple.xlsx",
  size: "9 ko",
}
const filePreviews = {
  success: "importer_des_bilans_detailles_siret_2026_exemple_fichier_accepte.jpg?v=2",
  altSuccess: "Exemple de fichier accepté pour importer des bilans détaillés, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "importer_des_bilans_detailles_siret_2026_exemple_fichier_rejete.jpg?v=3",
  altError: "Exemple de fichier rejeté pour importer des bilans détaillés, qui contient des erreurs dans les colonnes ou les valeurs",
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
    :filePreviews
    :links
    apiUrl="importDiagnostics/complete"
    schemaVersion="2026"
    :successMessage
  >
    Notre outil d’import de masse vous permet d’ajouter les bilans détaillés de toutes vos cantines d’un coup.
  </LayoutImport>
</template>
