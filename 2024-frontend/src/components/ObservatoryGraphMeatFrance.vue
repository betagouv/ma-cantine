<script setup>
import { reactive, computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import stringsService from "@/services/strings"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["meatFrancePercent"])
const storeFilters = useStoreFilters()
const title = "Viandes d'origine France"
const stats = reactive([props.meatFrancePercent])
const description = computed(() => {
  const filters = storeFilters.getSelectionLabels()
  const percent = stringsService.prettyPercent(stats[0])
  return `Pour la recherche ${filters}, le pourcentage de "${title}" est : ${percent}.`
})
</script>
<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="stats" :description="description">
    <GraphGauge :stats="stats" />
  </GraphBase>
</template>
