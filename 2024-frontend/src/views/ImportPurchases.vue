<script setup>
import { ref } from "vue"
import ImportExplanation from "@/components/ImportExplanation.vue"
import ImportHelp from "@/components/ImportHelp.vue"
import ImportSchemaTable from "@/components/ImportSchemaTable.vue"
import ImportSuccessModal from "@/components/ImportSuccessModal.vue"
import ImportFileUpload from "@/components/ImportFileUpload.vue"

/* Data */
const schemaFile = "achats.json"
const exampleFile = {
  name: "achats_fichier_exemple_ma_cantine.csv",
  size: "189 octets",
}

/* Sucess */
const showModal = ref(false)
const purchaseCount = ref(0)

const success = (count) => {
  purchaseCount.value = count
  showModal.value = true
}
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
  <ImportExplanation :exampleFile />
  <ImportSchemaTable :schemaFile />
  <ImportFileUpload @success="success" apiUrl="importPurchases" eventMatomo="import-purchases-success" />
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
