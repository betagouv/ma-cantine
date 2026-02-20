<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportHelp from "@/components/ImportHelp.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"

/* Router */
const route = useRoute()

/* Data */
const schemaFile = "bilans_detaille.json"
const exampleFile = {
  name: "importer_des_bilans_detailles_exemple.xlsx",
  size: "9 ko",
}
const links = [
  {
    title: "Liste des champs à renseigner pour importer un bilan détaillé",
    href: documentation.importBilanDetaille,
  },
  {
    title: "Aide pour les formats d'import CSV, Excel, ODS",
    href: documentation.importsFormatsFichiers,
  }
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
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload @success="success" apiUrl="importDiagnostics/complete" eventMatomo="import-diagnostics-complete-success"/>
  <ImportSuccessModal
    :opened="showModal"
    :message="successMessage"
    @close="showModal = false"
  />
  <ImportHelp />
</template>
