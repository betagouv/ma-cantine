<script setup>
import { ref } from "vue"
import { importCanteens } from "@/services/imports.js"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportStaffMention from "@/components/ImportStaffMention.vue"

/* Data */
const schemaUrl =
  "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/staging/data/schemas/imports/cantines.json"
const ressources = [
  {
    download: "fichier_exemple_ma_cantine_no_diag.csv",
    href: "/static/documents/fichier_exemple_ma_cantine_no_diag.csv",
    name: "Télécharger notre fichier d’exemple CSV",
    size: "496 octets",
  },
  {
    external: true,
    href: "https://ma-cantine.crisp.help/fr/article/comment-importer-un-fichier-csv-dans-excel-7zyxo/",
    name: "Comment importer un fichier CSV dans Excel ?",
  },
  {
    external: true,
    href: "https://ma-cantine.crisp.help/fr/article/comment-enregistrer-un-fichier-excel-en-csv-cgfrbp/",
    name: "Comment enregistrer mon fichier Excel en CSV ?",
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
  <h1>Importer des cantines</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet de créer vos cantines ou de modifier vos cantines existantes d’un coup.
    <strong>Il concerne uniquement les gestionnaires qui ont plus de 5&nbsp;cantines.</strong>
    Si vous avez moins de 5 cantines vous pouvez créer ou modifier des cantines depuis
    <router-link :to="{ name: 'NewCanteen' }">notre formulaire</router-link>
    .
  </p>
  <ImportExplanation :ressources />
  <ImportSchemaTable :url="schemaUrl" />
  <ImportStaffMention class="fr-mb-3w" />
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
</template>
