<script setup>
import { ref } from "vue"
import { importCanteens } from "@/services/imports.js"
import { useRootStore } from "@/stores/root"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportStaffCallout from "@/components/ImportStaffCallout.vue"
import ImportHelp from "@/components/ImportHelp.vue"

/* Store */
const store = useRootStore()

/* Data */
const schemaUrl =
  "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/staging/data/schemas/imports/cantines.json"
const exampleFile = {
  download: "fichier_exemple_ma_cantine_no_diag.csv",
  href: "/static/documents/fichier_exemple_ma_cantine_no_diag.csv",
  size: "496 octets",
}

/* Success */
const showModal = ref(false)
const canteenCount = ref(0)

const success = (count) => {
  canteenCount.value = count
  showModal.value = true
}
</script>

<template>
  <h1>Importer des cantines</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet de créer vos cantines ou de modifier vos cantines existantes d’un coup.
    <strong>Il concerne uniquement les gestionnaires qui ont plus de 5&nbsp;cantines.</strong>
    Si vous avez moins de 5 cantines vous pouvez créer ou modifier des cantines depuis
    <router-link :to="{ name: 'NewCanteen' }">notre formulaire</router-link>
    .
  </p>
  <ImportExplanation :exampleFile />
  <ImportSchemaTable :url="schemaUrl" />
  <ImportStaffCallout v-if="store.loggedUser.isStaff" class="fr-mb-3w" />
  <ImportFileUpload @success="success" :importFile="importCanteens" eventMatomo="import-canteen-success" />
  <ImportSuccessModal
    :opened="showModal"
    :message="
      canteenCount > 1
        ? 'Vos cantines sont enregistrées et sont maintenant disponibles.'
        : 'Votre cantine est enregistrée et est maintenant disponible.'
    "
    @close="showModal = false"
  />
  <ImportHelp />
</template>
