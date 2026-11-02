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
const schemaFile = "bilans_detaille_id_2026.json"
const exampleFile = {
  name: "importer_des_bilans_detailles_id_2026_exemple.xlsx",
  size: "8 ko",
}
const filePreviews = {
  success: "importer_des_bilans_detailles_id_2026_exemple_fichier_accepte.jpg?v=1",
  altSuccess: "Exemple de fichier accepté pour importer des bilans détaillés avec identification de la cantine via son ID, qui contient le bon nom de colonnes et les bonnes valeurs",
  error: "importer_des_bilans_detailles_id_2026_exemple_fichier_rejete.jpg?v=1",
  altError: "Exemple de fichier rejeté pour importer des bilans détaillés avec identification de la cantine via son ID, qui contient des erreurs dans les colonnes ou les valeurs",
}
const links = [
  {
    title: "Liste des champs à renseigner pour importer un bilan détaillé",
    href: documentation.importBilanDetaille,
  },
  {
    title: "Où trouver l'ID de ma cantine ou de mon groupe ?",
    href: documentation.trouverIdCantine,
  },
]

/* Sucess */
const showModal = ref(false)
const diagnosticsCount = ref(0)
const successMessage = ref("")

const success = (count) => {
  diagnosticsCount.value = count
  successMessage.value = count > 1 ? `Les ${count} bilans détaillés ont été importés avec succès` : 'Le bilan détaillé a été importé avec succès'
  showModal.value = true
}
</script>

<template>
  <h1>{{ route.meta.title }}</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet d’ajouter les bilans détaillés de toutes vos cantines d’un coup.
  </p>
  <ImportExplanation :exampleFile :links />
  <ImportFilesExample :filePreviews />
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload
    @success="success"
    apiUrl="importDiagnostics/complete"
    apiImportType="id"
    schemaVersion="2026"
    eventMatomo="import-diagnostics-complete-id-success"
  />
  <ImportSuccessModal
    :opened="showModal"
    :message="successMessage"
    @close="showModal = false"
  />
  <ImportHelp />
</template>
