<script setup>
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import CanteenSidebarTitle from "@/components/CanteenSidebarTitle.vue"
import CanteenListTeledeclarations from "@/components/CanteenListTeledeclarations.vue"

const route = useRoute()
const { canteenInformations } = storeToRefs(useStoreCanteen())
</script>

<template>
  <CanteenSidebarTitle :title="route.meta.title" />
  <CanteenListTeledeclarations
    class="fr-mt-md-n4w"
    :diagnostics="canteenInformations.diagnostics"
    :groupeDiagnostics="canteenInformations.centralKitchenDiagnostics"
    :canteenId="canteenInformations.id"
  />
</template>
