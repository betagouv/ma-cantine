<script setup>
import { computed, reactive } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["egalimPercent", "egalimObjective", "bioPercent", "bioObjective"])
const storeFilters = useStoreFilters()
const title = "Produits durables et de qualité dont les produits bio"
const objectives = reactive([
  {
    name: props.egalimObjective ? `${props.egalimObjective}%` : "50%",
    value: props.egalimObjective || 50,
  },
  {
    name: props.bioObjective ? `${props.bioObjective}%` : "20%",
    value: props.bioObjective || 20,
  },
])
const stats = reactive([props.egalimPercent, props.bioPercent])
const legends = ["durables et de qualité dont bio", "bio et en conversion bio"]

/* Description */
const getResultsDescription = () => {
  const resultWithObjectif = []
  for (let i = 0; i < stats.length; i++) {
    resultWithObjectif.push(
      `pour l'objectif "${legends[i]}" fixé à ${objectives[i].value}% le résultat est ${stats[i]}%`
    )
  }
  return resultWithObjectif.join(", ")
}
const description = computed(() => {
  const filters = storeFilters.getSelectionLabels()
  const results = getResultsDescription()
  return `Pour la recherche ${filters}, le pourcentage de "${title}" est : ${results}.`
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="stats" :description="description">
    <GraphGauge :objectives="objectives" :stats="stats" :legends="legends" />
  </GraphBase>
</template>
