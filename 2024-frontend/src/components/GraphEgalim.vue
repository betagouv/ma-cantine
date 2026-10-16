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
  "year",
  "descriptionCustom",
])
const title = "Objectifs EGalim"
const gauges = computed(() => {
  const allGauges = [
    {
      label: `au moins ${stringsService.prettyPercent(props.bioObjective)} d’achats Bio ou en conversion`,
      mention: props.mention,
      stat: props.bioPercent,
      objective: props.bioObjective,
      color: "var(--ma-cantine-color-bio)",
    },
    {
      hidden: Number(props.year) !== 2026,
      label: `au moins ${stringsService.prettyPercent(30)} d’achats SIQO, HVE ou fermier`,
      disabled: `le seuil des ${stringsService.prettyPercent(30)} SIQO, HVE ou fermiers sera comptabilisé dès implémentation des nouvelles catégories UPSA à partir des achats du 1er janvier 2027 pour télédéclaration en 2028`,
    },
    {
      label: `au moins ${stringsService.prettyPercent(props.egalimObjective)} d’achats EGalim dont bio`,
      stat: props.egalimPercent,
      objective: props.egalimObjective,
      color: "var(--ma-cantine-color-egalim)",
    },
    {
      label: `au moins ${stringsService.prettyPercent(60)} d’achats EGalim sur les familles viandes et poissons (${stringsService.prettyPercent(100)} pour les restaurants d'État)`,
      stat: props.viandesPoissonsEgalimPercent,
      objective: 60,
      color: "var(--ma-cantine-color-viandes-poissons)",
    },
  ]
  const displayedGauges = allGauges.filter((gauge) => !gauge.hidden)
  return displayedGauges
})

/* Description */
const getResultsDescription = () => {
  return gauges.value
    .map((gauge) => {
      const result = gauge.disabled || `le résultat est ${stringsService.prettyPercent(gauge.stat)}`
      return `pour l'objectif "${gauge.label}" ${result}`
    })
    .join(" ; ")
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
      :disabled="gauge.disabled"
      :color="gauge.color"
    />
  </GraphBase>
</template>
