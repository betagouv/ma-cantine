<script setup>
import { computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphPie from "@/components/GraphPie.vue"
import GraphBase from "@/components/GraphBase.vue"
import cantines from "@/data/cantines.json"

const props = defineProps(["managementTypes", "canteensCount"])
const storeFilters = useStoreFilters()
const title = "Mode de gestion"

/* Calculate graph props */
const graph = computed(() => {
  const managementTypesNames = Object.keys(props.managementTypes)
  const legends = []
  const percents = []
  for (let i = 0; i < managementTypesNames.length; i++) {
    const managementType = managementTypesNames[i]
    const isEmpty = props.managementTypes[managementType] === 0
    if (!isEmpty) {
      const count = props.managementTypes[managementType]
      const percent = Math.round((count / props.canteensCount) * 100)
      const index = cantines.managementType.findIndex((element) => element.apiName === managementType)
      const canteen = count > 1 ? "cantines" : "cantine"
      const type = index > -1 ? `En gestion ${cantines.managementType[index].label.toLowerCase()}` : "Inconnu"
      const legend = `${type} soit ${count} ${canteen}`
      percents.push(percent)
      legends.push(legend)
    }
  }
  if (percents.length === 0) {
    percents.push(100)
    legends.push("Inconnu")
  }
  return {
    legends,
    percents,
  }
})

/* Description */
const getResultsDescription = () => {
  const results = []
  for (let i = 0; i < graph.value.percents.length; i++) {
    results.push(`${graph.value.percents[i]}% ${graph.value.legends[i].toLocaleLowerCase()}`)
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
  <GraphBase :valuesToVerify="graph.percents" :description="description">
    <GraphPie :percents="graph.percents" :legends="graph.legends" />
  </GraphBase>
</template>
