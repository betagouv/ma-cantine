<script setup>
import { useRoute } from "vue-router"
import LayoutSidebarCanteen from "@/layouts/LayoutSidebarCanteen.vue"
import CanteenListTeledeclarations from "@/components/CanteenListTeledeclarations.vue"

const route = useRoute()
</script>

<template>
  <LayoutSidebarCanteen>
    <template #titleName>
      <h2 class="fr-h3 fr-mb-0">{{ route.meta.title }}</h2>
    </template>
    <template #content="{ canteenInformation }">
      <CanteenListTeledeclarations class="fr-mt-n4w" :diagnostics="canteenInformation?.diagnostics" :groupeDiagnostics="canteenInformation?.centralKitchenDiagnostics" :canteenId="canteenInformation?.id" />
    </template>
  </LayoutSidebarCanteen>
</template>
