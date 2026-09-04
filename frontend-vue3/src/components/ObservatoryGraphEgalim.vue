<script setup>
import { computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import stringsService from "@/services/strings"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["approPercent"])
const storeFilters = useStoreFilters()
const title = "Télédéclarations qui ont atteint l'objectif EGalim"
const description = computed(() => {
  const filters = storeFilters.getSelectionLabels()
  const percent = stringsService.prettyPercent(props.approPercent)
  return `Pour la recherche ${filters}, le pourcentage de "${title}" est : ${percent}.`
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[approPercent]" :description="description">
    <GraphGauge :stats="[approPercent]" />
  </GraphBase>
</template>
