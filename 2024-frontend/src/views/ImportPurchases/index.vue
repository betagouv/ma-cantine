<script setup>
import { ref } from "vue"

import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportHelpContact from "@/components/ImportHelpContact.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"

/* Data */
const schemaUrl =
  "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/staging/data/schemas/imports/achats.json"
const ressources = [
  {
    download: "achats_fichier_exemple_ma_cantine.csv",
    href: "/static/documents/achats_fichier_exemple_ma_cantine.csv",
    name: "Télécharger notre fichier d’exemple CSV",
    size: "189 octets",
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

/* Sucess */
// à renommer en faisant un lien avec la modal
const importSuccess = ref(false)
const purchaseCount = ref(0)

</script>

<template>
  <h1>Importer des achats</h1>
  <p class="fr-col-12 fr-col-md-7">
    Notre outil d’import de masse vous permet d’ajouter les achats de toutes vos cantines d’un coup.
    <strong>Si vous avez moins de 10 achats,</strong>
    il est plus rapide de les saisir directement
    <router-link :to="{ name: 'PurchasesHome' }">sur la plateforme</router-link>
    .
  </p>
  <ImportExplanation :ressources="ressources" />
  <ImportSchemaTable :url="schemaUrl" />
  <ImportFileUpload />
  <ImportSuccessModal
    :opened="importSuccess"
    :message="
      purchaseCount > 1
        ? 'Vos achats sont enregistrés et sont maintenant disponibles.'
        : 'Votre achat est enregistré et est maintenant disponible.'
    "
    @close="importSuccess = false"
  />
  <ImportHelpContact class="fr-mt-8w" />
</template>
