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
  "title",
])
const objectives = computed(() => [
  {
    name: stringsService.prettyPercent(props.egalimObjective),
    value: props.egalimObjective,
  },
  {
    name: stringsService.prettyPercent(props.bioObjective),
    value: props.bioObjective,
  },
])
const stats = computed(() => [props.egalimPercent, props.bioPercent])
const legends = ["EGalim dont bio", "bio et en conversion bio"]
const viandesPoissonsObjectives = [
  { name: stringsService.prettyPercent(60), value: 60 },
  { name: `${stringsService.prettyPercent(100)} pour les restaurants d'État`, value: 100 },
]

/* Description */
const getResultsDescription = () => {
  const resultWithObjectif = []
  for (let i = 0; i < stats.value.length; i++) {
    const objectifPercent = stringsService.prettyPercent(objectives.value[i].value)
    const resultPercent = stringsService.prettyPercent(stats.value[i])
    resultWithObjectif.push(
      `pour l'objectif "${legends[i]}" fixé à ${objectifPercent} le résultat est ${resultPercent}`
    )
  }
  const viandesPoissonsObjectifName = `${viandesPoissonsObjectives[0].name} et ${viandesPoissonsObjectives[1].name}`
  const viandesPoissonsPercent = stringsService.prettyPercent(props.viandesPoissonsEgalimPercent)
  resultWithObjectif.push(
    `pour l'objectif "EGalim viandes et poissons" fixé à ${viandesPoissonsObjectifName} le résultat est ${viandesPoissonsPercent}`
  )
  return resultWithObjectif.join(", ")
}
const description = computed(() => {
  const intro = [props.title, props.descriptionCustom].filter(Boolean).join(", ") || "Pour le graphique"
  const results = getResultsDescription()
  return `${intro} : ${results}.`
})
</script>

<template>
  <h3 v-if="title" class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[egalimPercent, bioPercent, viandesPoissonsEgalimPercent, egalimObjective, bioObjective]" :description="description">
    <GraphGauge
      :stat="egalimPercent"
      :objective="egalimObjective"
      :label="`au moins ${stringsService.prettyPercent(egalimObjective)} d’achats EGalim dont bio`"
      color="#1F7046"
    />
    <GraphGauge
      :stat="bioPercent"
      :objective="bioObjective"
      :label="`au moins ${stringsService.prettyPercent(bioObjective)} d’achats Bio ou en conversion`"
      color="#8AE4B3"
    />
    <GraphGauge
      :stat="viandesPoissonsEgalimPercent"
      :objective="viandesPoissonsObjectives[0].value"
      :label="`au moins ${viandesPoissonsObjectives[0].name} d’achats EGalim sur les familles viandes et poissons (${viandesPoissonsObjectives[1].name})`"
      color="#695240"
    />
  </GraphBase>
</template>
