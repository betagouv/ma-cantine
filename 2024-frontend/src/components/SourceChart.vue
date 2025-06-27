<script setup>
import { computed, ref } from "vue"
import { formatNumber, getPercentage } from "@/utils"
import Constants from "@/constants.js"

const props = defineProps(["measurement"])

const measurementPercentageValues = computed(() => {
  const m = props.measurement
  const canCalculatePercentage = m && m.totalMass
  const hasAtLeastOneSource = m.preparationTotalMass || m.unservedTotalMass || m.leftoversTotalMass
  if (canCalculatePercentage && hasAtLeastOneSource) {
    return {
      preparation: getPercentage(m.preparationTotalMass, m.totalMass),
      unserved: getPercentage(m.unservedTotalMass, m.totalMass),
      leftovers: getPercentage(m.leftoversTotalMass, m.totalMass),
    }
  }
  return undefined
})

const measurementGraphValues = computed(() => {
  return {
    y: JSON.stringify([[
      props.measurement.preparationTotalMass,
      props.measurement.unservedTotalMass,
      props.measurement.leftoversTotalMass,
    ]]),
    x: JSON.stringify([[
      Constants.WasteMeasurement.preparation.title,
      Constants.WasteMeasurement.unserved.title,
      Constants.WasteMeasurement.leftovers.title,
    ]]),
    name: JSON.stringify([
      Constants.WasteMeasurement.preparation.title,
      Constants.WasteMeasurement.unserved.title,
      Constants.WasteMeasurement.leftovers.title,
    ]),
  }
})

const displayOption = ref("chart")
</script>

<template>
  <div v-if="measurementPercentageValues">
    <div class="fr-grid-row">
      <div class="fr-col-md-7 fr-mb-2w">
        <h3 class="fr-h6 fr-my-0">Origine du gaspillage</h3>
      </div>
      <div class="fr-col fr-mb-2w" style="text-align: right;">
        <DsfrSegmentedSet
          name="Origine du gaspillage"
          label="Choix d'affichage"
          :options="[
            {
              label: 'Graphe',
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
        :name="measurementGraphValues.name"
        :x="measurementGraphValues.x"
        :y="measurementGraphValues.y"
        unit-tooltip="%"
      ></pie-chart>
    </div>
    <div v-else-if="displayOption === 'text'">
      <ul>
        <li>
          {{ Constants.WasteMeasurement.preparation.title }} : {{ formatNumber(measurement.preparationTotalMass) }} kg,
          soit {{ formatNumber(measurementPercentageValues.preparation) }} %
        </li>
        <li>
          {{ Constants.WasteMeasurement.unserved.title }} : {{ formatNumber(measurement.unservedTotalMass) }} kg, soit
          {{ formatNumber(measurementPercentageValues.unserved) }} %
        </li>
        <li>
          {{ Constants.WasteMeasurement.leftovers.title }} : {{ formatNumber(measurement.leftoversTotalMass) }} kg, soit
          {{ formatNumber(measurementPercentageValues.leftovers) }} %
        </li>
      </ul>
    </div>
  </div>
  <DsfrAlert v-else>
    Completez l'évaluation pour visualiser les sources de votre gaspillage.
  </DsfrAlert>
</template>
