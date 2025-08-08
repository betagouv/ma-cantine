<script setup>
import { ref } from "vue"
import { useStoreFilters } from "@/stores/filters.js"
import AppCode from "@/components/AppCode.vue"

const opened = ref(false)
const iconShare = "fr-icon-share-line"
const storeFilters = useStoreFilters()
const selectedFilters = storeFilters.getSelectionLabels()
const url = ref()

const openModal = () => {
  opened.value = true
  url.value = window.location.href
}
</script>
<template>
  <div class="fr-grid-row fr-grid-row--right">
    <DsfrButton label="Partager ma recherche" secondary :icon="iconShare" @click="openModal" />
  </div>
  <DsfrModal title="Partager la recherche" :opened="opened" :icon="iconShare" @close="opened = false">
    <template #default>
      <p>Pour partager les chiffres clés de votre recherche : {{ selectedFilters }}</p>
      <p class="ma-cantine--bold fr-mb-1w">Copier l'url :</p>
      <AppCode :content="url" />
    </template>
  </DsfrModal>
</template>
