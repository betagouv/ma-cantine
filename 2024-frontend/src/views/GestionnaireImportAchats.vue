<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportHelp from "@/components/ImportHelp.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportFilesExample from "@/components/ImportFilesExample.vue"

/* Router */
const route = useRoute()

/* Data */
const schemaFile = "achats_id.json"
const exampleFile = {
  name: "achats_fichier_exemple_ma_cantine.xlsx",
  size: "6 ko",
}
const filePreviews = {
  success: "achats_fichier_exemple_fichier_accepte.jpg?v=4",
  altSuccess: "Exemple de fichier accepté pour importer des achats, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "achats_fichier_exemple_fichier_rejete.jpg?v=4",
  altError: "Exemple de fichier rejeté pour importer des achats, qui contient des erreurs dans les colonnes ou les valeurs",
}
const links = [
  {
    title: "Où trouver l'ID de ma cantine ou de mon groupe ?",
    href: documentation.trouverIdCantine,
  },
  {
    title: "Aide pour les formats d'import CSV, Excel, ODS",
    href: documentation.importsFormatsFichiers,
  }
]

/* Sucess */
const showModal = ref(false)
const purchaseCount = ref(0)

const success = (count) => {
  purchaseCount.value = count
  showModal.value = true
}
</script>

<template>
  <h1>{{ route.meta.title }}</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet d’ajouter les achats de toutes vos cantines d’un coup.
    <strong>Si vous avez moins de 10 achats,</strong>
    il est plus rapide de les saisir directement
    <router-link :to="{ name: 'PurchasesHome' }">sur la plateforme</router-link>
    .
  </p>
  <ImportExplanation :exampleFile :links />
  <ImportFilesExample :filePreviews />
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload @success="success" apiUrl="importPurchases" apiImportType="id" eventMatomo="import-purchases-id-success"/>
  <ImportSuccessModal
    :opened="showModal"
    :message="
      purchaseCount > 1
        ? 'Vos achats sont enregistrés et sont maintenant disponibles.'
        : 'Votre achat est enregistré et est maintenant disponible.'
    "
    @close="showModal = false"
  />
  <ImportHelp />
</template>
