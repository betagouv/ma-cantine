<script setup>
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import AppSeparator from "@/components/AppSeparator.vue"
import CanteenListTeledeclarations from "@/components/CanteenListTeledeclarations.vue"

const route = useRoute()
const { canteenInformations } = storeToRefs(useStoreCanteen())
</script>

<template>
  <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-mt-2w fr-mt-md-0 fr-mb-2w fr-mb-md-0">
    <h2 class="fr-h3 fr-mb-0">{{ route.meta.title }}</h2>
  </div>
  <AppSeparator class="layout-sidebar-canteen__separator fr-mt-3w fr-mb-5w" />
  <CanteenListTeledeclarations
    class="fr-mt-md-n4w"
    :diagnostics="canteenInformations.diagnostics"
    :groupeDiagnostics="canteenInformations.centralKitchenDiagnostics"
    :canteenId="canteenInformations.id"
  />
</template>
