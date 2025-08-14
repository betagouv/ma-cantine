<script setup>
import { computed } from "vue"
import { useStoreFilters } from "@/stores/filters"
import GraphPie from "@/components/GraphPie.vue"
import GraphBase from "@/components/GraphBase.vue"
import cantines from "@/data/cantines.json"

const props = defineProps(["sectorCategories", "canteensCount"])
const storeFilters = useStoreFilters()
const title = "Segments de secteurs"

/* Calculate graph props */
const graph = computed(() => {
  const sectorCategoriesName = Object.keys(props.sectorCategories)
  const legends = []
  const percents = []
  for (let i = 0; i < sectorCategoriesName.length; i++) {
    const sectorCategorie = sectorCategoriesName[i]
    const isEmpty = props.sectorCategories[sectorCategorie] === 0
    if (!isEmpty) {
      const count = props.sectorCategories[sectorCategorie]
      const percent = Math.round((count / props.canteensCount) * 100)
      const canteen = count > 1 ? "cantines" : "cantine"
      const type = cantines.sectorCategorie[sectorCategorie] || "Non renseigné"
      const legend = `${type} soit ${count} ${canteen}`
      percents.push(percent)
      legends.push(legend)
    }
  }
  if (percents.length === 0) {
    percents.push(100)
    legends.push("Non renseigné")
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
    <GraphPie :percents="graph.percents" :legends="graph.legends" alignment="horizontal" />
  </GraphBase>
</template>
