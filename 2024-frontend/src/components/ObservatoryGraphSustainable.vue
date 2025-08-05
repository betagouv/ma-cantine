<script setup>
import { computed, reactive } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["egalimPercent", "bioPercent"])
const storeFilters = useStoreFilters()
const title = "Produits durables et de qualité dont les produits bio"

/* Graph properties */
const objectives = [
  { name: "50%", value: 50 },
  { name: "20%", value: 20 },
]
const stats = reactive([props.egalimPercent, props.bioPercent])
const legends = ["durables et de qualité dont bio", "bio et en conversion bio"]

/* Function to generate descriptions */
const getFiltersDescription = () => {
  const selected = storeFilters.getSelection().map((item) => item.label)
  const list = selected.join(", ")
  return `Pour la recherche ${list}`
}
const getResultsDescription = () => {
  const resultWithObjectif = []
  for (let i = 0; i < stats.length; i++) {
    resultWithObjectif.push(`objectif "${legends[i]}" fixé à ${objectives[i].value}% le résultat est ${stats[i]}%`)
  }
  return resultWithObjectif.join(", ")
}

/* Graph description */
const description = computed(() => {
  const filtersDescription = getFiltersDescription()
  const resultsDescription = getResultsDescription()
  return `${filtersDescription}, les résultats du graphique "${title}" sont : ${resultsDescription}.`
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="stats" :description="description">
    <GraphGauge :objectives="objectives" :stats="stats" :legends="legends" />
  </GraphBase>
</template>
