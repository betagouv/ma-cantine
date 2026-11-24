<script setup>
import documentation from "@/data/documentation.json"
import LayoutImport from "@/layouts/LayoutImport.vue"

/* Data */
const schemaFile = "cantines_modifier.json"
const exampleFile = {
  name: "importer_des_cantines_modifier_exemple_ma_cantine.xlsx",
  size: "6 ko",
}
const filePreviews = {
  success: "importer_des_cantines_modifier_exemple_fichier_accepte.jpg",
  altSuccess: "Exemple de fichier accepté pour modifier des cantines, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "importer_des_cantines_modifier_exemple_fichier_rejete.jpg",
  altError: "Exemple de fichier rejeté pour modifier des cantines, qui contient des erreurs dans les colonnes ou les valeurs",
}
const links = [
  {
    title: "Où trouver le numéro ID de ma cantine ?",
    href: documentation.trouverIdCantine,
  },
  {
    title: "Bien calculer son nombre de couverts",
    href: documentation.calculerNombreCouverts,
  },
]

/* Success */
const successMessage = (count) => count > 1
  ? "Vos cantines sont modifiées et sont maintenant disponibles dans votre tableau de bord."
  : "Votre cantine est modifiée et est maintenant disponible dans votre tableau de bord."
</script>

<template>
  <LayoutImport
    :schemaFile
    :exampleFile
    :filePreviews
    :links
    :adminCallout="true"
    apiUrl="importCanteens/update"
    :successMessage
  >
    Notre outil d'import de masse vous permet de modifier vos cantines d'un coup via leur numéro ID.
    Vous pouvez modifier des cantines inscrites avec leur numéro SIRET ou avec le numéro SIREN d'une unité légale.
  </LayoutImport>
</template>
