<script setup>
import LayoutImport from "@/layouts/LayoutImport.vue"
import ImportDeprecatedWarningPurchases from "@/components/ImportDeprecatedWarningPurchases.vue"

/* Data */
const schemaFile = "achats_siret_old.json"
const exampleFile = {
  name: "achats_siret_ancien_format_fichier_exemple_ma_cantine.xlsx",
  size: "6 ko",
}
const filePreviews = {
  success: "achats_siret_ancien_format_fichier_exemple_fichier_accepte.jpg?v=5",
  altSuccess: "Exemple de fichier accepté pour importer des achats, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "achats_siret_ancien_format_fichier_exemple_fichier_rejete.jpg?v=5",
  altError: "Exemple de fichier rejeté pour importer des achats, qui contient des erreurs dans les colonnes ou les valeurs",
}

/* Success */
const successMessage = (count) => count > 1
  ? "Vos achats sont enregistrés et sont maintenant disponibles."
  : "Votre achat est enregistré et est maintenant disponible."
</script>

<template>
  <LayoutImport
    :schemaFile
    :exampleFile
    :filePreviews
    apiUrl="importPurchasesOld"
    apiImportType="siret"
    :successMessage
  >
    <template #warning>
      <ImportDeprecatedWarningPurchases :redirectTo="{ name: 'GestionnaireImportAchatsSIRET' }" />
    </template>
    Notre outil d’import de masse vous permet d’ajouter les achats de toutes vos cantines d’un coup.
    <strong>Si vous avez moins de 10 achats,</strong>
    il est plus rapide de les saisir directement
    <router-link :to="{ name: 'PurchasesHome' }">sur la plateforme</router-link>
    .
  </LayoutImport>
</template>
