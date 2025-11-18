<script setup>
import { computed, reactive } from "vue"
import { useStoreFilters } from "@/stores/filters"
import stringsService from "@/services/strings"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["meatFishEgalimPercent"])
const storeFilters = useStoreFilters()
const title = "Viandes, volailles et produits d'aquaculture"
const objectives = [
  { name: stringsService.prettyPercent(60), value: 60 },
  { name: `${stringsService.prettyPercent(100)} pour les restaurants d'État`, value: 100 },
]
const stats = reactive([props.meatFishEgalimPercent])
const description = computed(() => {
  const filters = storeFilters.getSelectionLabels()
  const percent = stringsService.prettyPercent(stats[0])
  return `Pour la recherche ${filters}, le pourcentage de "${title}" avec un objectif fixé à ${objectives[0].name} et ${objectives[1].name} est : ${percent}.`
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[props.meatFishEgalimPercent]" :description="description">
    <GraphGauge :objectives="objectives" :stats="stats" />
  </GraphBase>
</template>
