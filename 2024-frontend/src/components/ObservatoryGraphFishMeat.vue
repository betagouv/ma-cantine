<script setup>
import { computed, reactive } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["meatPercent", "fishPercent"])
const storeFilters = useStoreFilters()
const title = "Viandes et volailles + produits d’aquacultures"

/* Graph properties */
const objectives = [
  { name: "60%", value: 60 },
  { name: "100% pour les restaurants d’état", value: 100 },
]
const stats = reactive([props.meatPercent + props.fishPercent])

/* Function to generate descriptions */
const getFiltersDescription = () => {
  const selected = storeFilters.getSelection().map((item) => item.label)
  const list = selected.join(", ")
  return `Pour la recherche ${list}`
}

/* Graph description */
const description = computed(() => {
  const filtersDescription = getFiltersDescription()
  const resultsDescription = `avec un objectif fixé à ${objectives[0].name} et ${objectives[1].name} est : ${stats[0]}%`
  return `${filtersDescription}, le résultat du graphique "${title}" ${resultsDescription}.`
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[props.meatPercent, props.fishPercent]" :description="description">
    <GraphGauge :objectives="objectives" :stats="stats" />
  </GraphBase>
</template>
