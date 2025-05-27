<script setup>
import { computed, ref } from "vue"
import { formatNumber, getSum, getPercentage } from "@/utils"

const props = defineProps(["measurement"])

const isEmpty = (value) => value === "" || value === null

const measurementComputedValues = computed(() => {
  const m = props.measurement
  const edibleMass = [m.preparationEdibleMass, m.unservedEdibleMass, m.leftoversEdibleMass]
  const edibleTotalMass = getSum(edibleMass)
  const edibleIsEmpty = edibleMass.every(isEmpty)
  const inedibleMass = [m.preparationInedibleMass, m.unservedInedibleMass, m.leftoversInedibleMass]
  const inedibleTotalMass = getSum(inedibleMass)
  const inedibleIsEmpty = inedibleMass.every(isEmpty)
  return {
    edible: {
      totalMass: edibleTotalMass,
      percentage: getPercentage(edibleTotalMass, m.totalMass),
      isEmpty: edibleIsEmpty,
    },
    inedible: {
      totalMass: inedibleTotalMass,
      percentage: getPercentage(inedibleTotalMass, m.totalMass),
      isEmpty: inedibleIsEmpty,
    },
  }
})

const measurementChartValues = computed(() => {
  return {
    y: JSON.stringify([
      measurementComputedValues.value.edible.totalMass,
      measurementComputedValues.value.inedible.totalMass,
    ]),
    x: JSON.stringify(["Comestible", "Non-comestible"]),
  }
})

const showChart = computed(
  () => !measurementComputedValues.value.edible.isEmpty && !measurementComputedValues.value.inedible.isEmpty
)

const displayOption = ref("chart")
</script>

<template>
  <div v-if="showChart">
    <div class="fr-grid-row">
      <div class="fr-col-md-7 fr-mb-2w">
        <h3 class="fr-h6 fr-my-0">Part de comestible</h3>
      </div>
      <div class="fr-col fr-mb-2w" style="text-align: right;">
        <DsfrSegmentedSet
          name="Part de comestible"
          label="Choix d'affichage"
          :options="[
            {
              label: 'Charte',
              value: 'chart',
            },
            {
              label: 'Texte',
              value: 'text',
            },
          ]"
          v-model="displayOption"
          small
        />
      </div>
    </div>
    <div v-if="displayOption === 'chart'" class="fr-py-2w fr-pr-8w">
      <pie-chart
        :name="measurementChartValues.x"
        :x="measurementChartValues.x"
        :y="measurementChartValues.y"
        color='["green-bourgeon", "orange-terre-battue"]'
      />
    </div>
    <div v-else-if="displayOption === 'text'">
      <ul>
        <li>
          Comestible : {{ formatNumber(measurementComputedValues.edible.totalMass) }} kg, soit
          {{ formatNumber(measurementComputedValues.edible.percentage) }} %
        </li>
        <li>
          Non-comestible : {{ formatNumber(measurementComputedValues.inedible.totalMass) }} kg, soit
          {{ formatNumber(measurementComputedValues.inedible.percentage) }} %
        </li>
      </ul>
    </div>
  </div>
  <DsfrAlert v-else>
    Completez l'évaluation pour visualiser la part de comestible de votre gaspillage.
  </DsfrAlert>
</template>
