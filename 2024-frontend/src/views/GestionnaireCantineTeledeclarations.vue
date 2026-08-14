<script setup>
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { computedAsync } from "@vueuse/core"
import { useStoreCanteen } from "@/stores/canteen.js"
import diagnosticService from "@/services/diagnostics.js"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import CanteenTeledeclarationPdf from "@/components/CanteenTeledeclarationPdf.vue"

const route = useRoute()
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const diagnostics = computedAsync(async () => await diagnosticService.fetchDiagnosticsRecap(canteenInformations.value.id),[])
</script>

<template>
  <CanteenSidebarTitle :title="route.meta.title" />
  <ul class="gestionnaire-cantine-teledeclarations ma-cantine--unstyled-list fr-mt-md-n4w">
    <CanteenTeledeclarationPdf
      v-for="diagnostic in diagnostics"
      :key="diagnostic"
      :diagnostic="diagnostic"
      :canteen-id="canteenInformations.id"
      class="gestionnaire-cantine-teledeclarations__item"
    />
  </ul>
</template>

<style lang="scss">
.gestionnaire-cantine-teledeclarations {
  &__item {
    border-bottom: solid 1px var(--border-disabled-grey);
  }
}
</style>
