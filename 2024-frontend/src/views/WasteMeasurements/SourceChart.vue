<script setup>
import { computed } from "vue"
import { formatNoValue } from "@/utils"

const props = defineProps(["measurement"])

const measurementPercentageValues = computed(() => {
  const m = props.measurement
  const canCalculatePercentage = m && m.totalMass
  const hasAtLeastOneSource = m.preparationTotalMass || m.unservedTotalMass || m.leftoversTotalMass
  if (canCalculatePercentage && hasAtLeastOneSource) {
    return {
      preparation: ((m.preparationTotalMass || 0) / m.totalMass) * 100,
      unserved: ((m.unservedTotalMass || 0) / m.totalMass) * 100,
      leftovers: ((m.leftoversTotalMass || 0) / m.totalMass) * 100,
      // TODO: other ?
    }
  }
  return undefined
})

const measurementGraphValues = computed(() => {
  return {
    y: JSON.stringify([
      props.measurement.preparationTotalMass,
      props.measurement.unservedTotalMass,
      props.measurement.leftoversTotalMass,
    ]),
    x: JSON.stringify(["Excédents de préparation", "Denrées non servies", "Reste-assiette"]),
  }
})
</script>

<template>
  <div v-if="measurementPercentageValues">
    <!-- TODO: accessible table view -->
    <pie-chart
      :name="measurementGraphValues.x"
      :x="measurementGraphValues.x"
      :y="measurementGraphValues.y"
      color='["purple-glycine", "green-archipel", "pink-tuile"]'
    ></pie-chart>
    <h3>Origine du gaspillage</h3>
    <ul>
      <li>Excédents de préparation : {{ formatNoValue(measurementPercentageValues.preparation) }} %</li>
      <li>Denrées présentées mais non servies : {{ formatNoValue(measurementPercentageValues.unserved) }} %</li>
      <li>Reste-assiette : {{ formatNoValue(measurementPercentageValues.leftovers) }} %</li>
    </ul>
  </div>
  <DsfrAlert v-else>
    Completez la saisie du pesage pour visualiser les sources de votre gaspillage.
  </DsfrAlert>
</template>
