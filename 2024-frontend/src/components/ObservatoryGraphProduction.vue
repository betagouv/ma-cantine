<script setup>
import { computed } from "vue"
import GraphPie from "@/components/GraphPie.vue"
import cantines from "@/data/cantines.json"

const props = defineProps(["productionTypes", "canteensCount"])
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
</script>

<template>
  <GraphPie :counts="counts" :total="canteensCount" :legends="legends" />
</template>
