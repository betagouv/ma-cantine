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
  "descriptionCustom",
])
const title = "Objectifs EGalim"
const gauges = computed(() => [
  {
    label: `au moins ${stringsService.prettyPercent(props.egalimObjective)} d’achats EGalim dont bio`,
    stat: props.egalimPercent,
    objective: props.egalimObjective,
    color: "#1F7046",
  },
  {
    label: `au moins ${stringsService.prettyPercent(props.bioObjective)} d’achats Bio ou en conversion`,
    stat: props.bioPercent,
    objective: props.bioObjective,
    color: "#8AE4B3",
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
  const intro = [title, props.descriptionCustom].filter(Boolean).join(", ")
  const results = getResultsDescription()
  return `${intro} : ${results}.`
})
</script>

<template>
  <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-my-2w">
    <h3 class="fr-h6 fr-mb-0">{{ title }}</h3>
    <p class="fr-text--sm fr-text-mention--grey fr-mb-0">sur {{ stringsService.prettyPercent(100) }} du Total des achats</p>
  </div>
  <GraphBase :valuesToVerify="[egalimPercent, bioPercent, viandesPoissonsEgalimPercent, egalimObjective, bioObjective]" :description="description">
    <GraphGauge
      v-for="gauge in gauges"
      :key="gauge.label"
      :stat="gauge.stat"
      :objective="gauge.objective"
      :label="gauge.label"
      :color="gauge.color"
    />
  </GraphBase>
</template>
