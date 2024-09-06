<script setup>
import { computed, ref } from "vue"
import { formatNumber, getPercentage } from "@/utils"

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
    y: JSON.stringify([
      props.measurement.preparationTotalMass,
      props.measurement.unservedTotalMass,
      props.measurement.leftoversTotalMass,
    ]),
    x: JSON.stringify(["Excédents de préparation", "Denrées non servies", "Reste-assiette"]),
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
      <div class="fr-col fr-mb-2w">
        <div class="fr-grid-row fr-grid-row--right">
          <DsfrSegmentedSet
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
    </div>
    <div v-if="displayOption === 'chart'" class="fr-py-2w fr-pr-8w">
      <pie-chart
        :name="measurementGraphValues.x"
        :x="measurementGraphValues.x"
        :y="measurementGraphValues.y"
        color='["blue-ecume", "yellow-moutarde", "pink-tuile"]'
      ></pie-chart>
    </div>
    <div v-else-if="displayOption === 'text'">
      <ul>
        <li>
          Excédents de préparation : {{ formatNumber(measurement.preparationTotalMass) }} kg, soit
          {{ formatNumber(measurementPercentageValues.preparation) }} %
        </li>
        <li>
          Denrées présentées mais non servies : {{ formatNumber(measurement.unservedTotalMass) }} kg, soit
          {{ formatNumber(measurementPercentageValues.unserved) }} %
        </li>
        <li>
          Reste-assiette : {{ formatNumber(measurement.leftoversTotalMass) }} kg, soit
          {{ formatNumber(measurementPercentageValues.leftovers) }} %
        </li>
      </ul>
    </div>
  </div>
  <DsfrAlert v-else>
    Completez l'évaluation pour visualiser les sources de votre gaspillage.
  </DsfrAlert>
</template>
