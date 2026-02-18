<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import documentation from "@/data/documentation.json"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
// import ImportFilesExample from "@/components/ImportFilesExample.vue"
import ImportHelp from "@/components/ImportHelp.vue"

/* Router */
const route = useRoute()

/* Data */
const schemaFile = "cantines_modifier.json"
const exampleFile = {
  name: "importer_des_cantines_modifier_exemple_ma_cantine.xlsx",
  size: "6 ko",
}
// const filePreviews = {
//   success: "",
//   altSuccess: "",
//   error: "",
//   altError: "",
// }
const links = [
  {
    title: "Où trouver le numéro ID de ma cantine ?",
    href: documentation.trouverIdCantine,
  },
  {
    title: "Aide pour les formats d'import CSV, Excel, ODS",
    href: documentation.importsFormatsFichiers,
  },
  {
    title: "Bien calculer son nombre de couverts",
    href: documentation.calculerNombreCouverts,
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
  <h1>{{ route.meta.title }}</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d'import de masse vous permet de modifier vos cantines d'un coup via leur numéro ID.
    Vous pouvez modifier des cantines inscrites avec leur numéro SIRET ou avec le numéro SIREN d'une unité légale.
  </p>
  <ImportExplanation :exampleFile :links />
  <!--
  <ImportFilesExample :filePreviews />
  -->
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload
    @success="success"
    apiUrl="importCanteens/update"
    eventMatomo="import-canteen-update-success"
  />
  <ImportSuccessModal
    :opened="showModal"
    :message="
      canteenCount > 1
        ? 'Vos cantines sont modifiées et sont maintenant disponibles dans votre tableau de bord.'
        : 'Votre cantine est modifiée et est maintenant disponible dans votre tableau de bord.'
    "
    @close="showModal = false"
  />
  <ImportHelp />
</template>
