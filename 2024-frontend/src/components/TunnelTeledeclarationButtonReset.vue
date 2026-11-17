<script setup>
import { useRoute } from "vue-router"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"

const route = useRoute()
const storeTeledeclaration = useStoreTeledeclaration()
const resetVolet = () => storeTeledeclaration.resetVolet(route.meta.volet)
</script>
<template>
  <div class="ma-cantine--flex-end fr-mt-2w">
    <DsfrButton
      secondary
      size="small"
      icon="fr-icon-refresh-line"
      label="Réinitialiser mes réponses"
      @click="resetVolet"
    />
  </div>
</template>
