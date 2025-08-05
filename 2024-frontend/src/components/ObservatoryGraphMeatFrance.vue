<script setup>
import { reactive, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["meatFrancePercent"])
const storeFilters = useStoreFilters()
const title = "Viandes d'origine France"
const stats = reactive([props.meatFrancePercent])

/* Graph description */
const description = computed(() => {
  const filters = storeFilters.getSelectionLabels()
  return `Pour la recherche ${filters}, le pourcentage de "${title}" est : ${stats[0]}%.`
})
</script>
<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="stats" :description="description">
    <GraphGauge :stats="stats" />
  </GraphBase>
</template>
