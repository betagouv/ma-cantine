<script setup>
import { computed, reactive } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["meatPercent", "fishPercent"])
const storeFilters = useStoreFilters()
const title = "Viandes, volailles et produits d’aquacultures"

/* Graph properties */
const objectives = [
  { name: "60%", value: 60 },
  { name: "100% pour les restaurants d’état", value: 100 },
]
const stats = reactive([props.meatPercent + props.fishPercent])

/* Graph description */
const description = computed(() => {
  const filters = storeFilters.getSelectionLabels()
  return `Pour la recherche ${filters}, le pourcentage de "${title}" avec un objectif fixé à ${objectives[0].name} et ${objectives[1].name} est : ${stats[0]}%.`
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[props.meatPercent, props.fishPercent]" :description="description">
    <GraphGauge :objectives="objectives" :stats="stats" />
  </GraphBase>
</template>
