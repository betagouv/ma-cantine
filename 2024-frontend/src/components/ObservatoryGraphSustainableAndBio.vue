<script setup>
import { computed, reactive } from "vue"
import AppGraph from "@/components/AppGraph.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["stats"])

/* Graph properties */
const objectives = [
  { name: "50%", value: 50 },
  { name: "20%", value: 20 },
]
const results = reactive([props.stats.sustainablePercent, props.stats.bioPercent])
const legends = ["durables et de qualité dont bio", "bio et en conversion bio"]

/* Graph description */
const description = computed(() => {
  let sentence = ""
  for (let i = 0; i < results.length; i++) {
    sentence += `Pour l'objectif "${legends[i]}" fixé à ${objectives[0].value}% le résultat est ${results[0]}%. `
  }
  return sentence
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">1. Produits durable et de qualité dont les produits bio</h3>
  <AppGraph :valuesToVerify="results" :description="description">
    <GraphGauge :objectives="objectives" :stats="results" :legends="legends" />
  </AppGraph>
</template>
