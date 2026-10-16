<script setup>
import { computed } from "vue"
import stringsService from "@/services/strings"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps([
  "egalimPercent",
  "egalimObjective",
  "bioPercent",
  "bioObjective",
  "viandesPoissonsEgalimPercent",
  "mention",
  "descriptionCustom",
])
const title = "Objectifs EGalim"
const gauges = computed(() => [
  {
    label: `au moins ${stringsService.prettyPercent(props.bioObjective)} d’achats Bio ou en conversion`,
    mention: props.mention,
    stat: props.bioPercent,
    objective: props.bioObjective,
    color: "#8AE4B3",
  },
  {
    label: `au moins ${stringsService.prettyPercent(props.egalimObjective)} d’achats EGalim dont bio`,
    stat: props.egalimPercent,
    objective: props.egalimObjective,
    color: "#1F7046",
  },
  {
    label: `au moins ${stringsService.prettyPercent(60)} d’achats EGalim sur les familles viandes et poissons (${stringsService.prettyPercent(100)} pour les restaurants d'État)`,
    stat: props.viandesPoissonsEgalimPercent,
    objective: 60,
    color: "#0974F6",
  },
])

/* Description */
const getResultsDescription = () => {
  return gauges.value
    .map((gauge) => `pour l'objectif "${gauge.label}" le résultat est ${stringsService.prettyPercent(gauge.stat)}`)
    .join(", ")
}
const description = computed(() => {
  const intro = props.descriptionCustom || "Pour le graphique"
  const results = getResultsDescription()
  return `${intro} : ${results}.`
})
</script>

<template>
  <h3 class="fr-h6 fr-my-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[egalimPercent, bioPercent, viandesPoissonsEgalimPercent, egalimObjective, bioObjective]" :description="description">
    <GraphGauge
      v-for="gauge in gauges"
      :key="gauge.label"
      :stat="gauge.stat"
      :objective="gauge.objective"
      :label="gauge.label"
      :mention="gauge.mention"
      :color="gauge.color"
    />
  </GraphBase>
</template>
