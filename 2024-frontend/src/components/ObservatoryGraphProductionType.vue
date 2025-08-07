<script setup>
import { computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphPie from "@/components/GraphPie.vue"
import GraphBase from "@/components/GraphBase.vue"
import cantines from "@/data/cantines.json"

const props = defineProps(["productionTypes", "canteensCount"])
const storeFilters = useStoreFilters()
const title = "Mode de production"

/* Calculate graph props */
const counts = computed(() => Object.values(props.productionTypes))
const legends = computed(() => {
  const legends = []
  const productionTypesNames = Object.keys(props.productionTypes)
  for (let i = 0; i < productionTypesNames.length; i++) {
    const value = productionTypesNames[i]
    const index = cantines.productionType.findIndex((element) => element.apiName === value)
    const legend = index > -1 ? cantines.productionType[index].hint : "Inconnu"
    legends.push(legend)
  }
  return legends
})
const percents = computed(() => {
  const percents = []
  for (let i = 0; i < counts.value.length; i++) {
    const percent = Math.round((counts.value[i] / props.canteensCount) * 100)
    percents.push(percent)
  }
  return percents
})

/* Description */
const getResultsDescription = () => {
  const results = []
  for (let i = 0; i < counts.value.length; i++) {
    const canteenCounts = counts.value[i]
    const canteen = canteenCounts > 1 ? "cantines" : "cantine"
    results.push(`${percents.value[i]}% "${legends.value[i]}", soit ${counts.value[i]} ${canteen}`)
  }
  return results.join(", ")
}
const description = computed(() => {
  const filters = storeFilters.getSelectionLabels()
  const results = getResultsDescription()
  return `Pour la recherche ${filters}, le pourcentage des cantines réparties par "${title}" est : ${results}.`
})
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[...counts, canteensCount]" :description="description">
    <GraphPie :percents="percents" :counts="counts" :legends="legends" />
  </GraphBase>
</template>
