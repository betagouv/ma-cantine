<script setup>
// import { ref } from "vue"
import { useRoute } from "vue-router"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportHelp from "@/components/ImportHelp.vue"
// import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
// import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
// import ImportFileUpload from "@/components/ImportFileUpload.vue"
// import ImportFilesExample from "@/components/ImportFilesExample.vue"

/* Router */
const route = useRoute()

/* Data */
// const schemaFile = "diagnostics_simple.json"
const exampleFile = {
  name: "importer_des_bilans_simplifies_exemple.csv",
  size: "606 octets",
}
// const filePreviews = {
//   success: "",
//   altSuccess: "",
//   error: "",
//   altError: "",
// }

/* Sucess */
// const showModal = ref(false)
// const purchaseCount = ref(0)

// const success = (count) => {
//   purchaseCount.value = count
//   showModal.value = true
// }
</script>

<template>
  <h1>{{ route.meta.title }}</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet d’ajouter les bilans simplifiés de toutes vos cantines d’un coup.
  </p>
  <ImportExplanation :exampleFile/>
  <!--
  <ImportFilesExample :filePreviews />
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload @success="success" apiUrl="" eventMatomo=""/>
  <ImportSuccessModal
    :opened="showModal"
    :message=""
    @close="showModal = false"
  />-->
  <ImportHelp />
</template>
