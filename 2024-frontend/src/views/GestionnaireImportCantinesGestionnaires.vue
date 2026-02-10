<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportHelp from "@/components/ImportHelp.vue"

/* Store and Router */
const route = useRoute()

/* Data */
const schemaFile = "cantines_gestionnaires.json"
const links = [
  {
    title: "Aide pour les formats d'import CSV, Excel, ODS",
    href: documentation.importsFormatsFichiers,
  },
]

/* Success */
const showModal = ref(false)
const canteenCount = ref(0)

const success = (count) => {
  canteenCount.value = count
  showModal.value = true
}
</script>

<template>
  <h1 class="fr-col-12 fr-col-md-7">{{ route.meta.title }}</h1>
  <ImportExplanation :links />
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload
    @success="success"
    apiUrl="importCanteensGestionnaires"
    eventMatomo="import-canteen-gestionnaires-success"
  />
  <ImportSuccessModal
    :opened="showModal"
    :message="
      canteenCount > 1
        ? 'Vos cantines sont modifiées.'
        : 'Votre cantine est modifiée.'
    "
    @close="showModal = false"
  />
  <ImportHelp />
</template>
