<script setup>
import { computed, ref } from "vue"
import EdibleChart from "./EdibleChart.vue"
import SourceChart from "./SourceChart.vue"
import MeasurementDetail from "./WasteMeasurementDetail.vue"
import EmphasiseText from "./EmphasiseText.vue"
import { formatNumber, formatDate } from "@/utils"

const props = defineProps(["measurement", "measurements", "editable", "canteenUrlComponent"])

const chosenMeasurementIdx = ref(0)
const displayMeasurement = computed(
  () => props.measurement || (props.measurements?.length && props.measurements[chosenMeasurementIdx.value])
)

const wastePerMeal = computed(() => {
  const m = displayMeasurement.value
  if (m && m.totalMass && m.mealCount) return (m.totalMass / m.mealCount) * 1000 // convert kg to g
  return undefined
})

const measurementChoices = computed(() => {
  return props.measurements.map((m, idx) => {
    return {
      text: `${formatDate(m.periodStartDate, {
        month: "short",
        day: "numeric",
      })} - ${formatDate(m.periodEndDate)}`,
      value: idx,
    }
  })
})

const newMeasurementRoute = {
  name: "GestionnaireGaspillageAlimentaireModifier",
  params: { canteenUrlComponent: props.canteenUrlComponent },
}

const measurementTunnel = computed(() => ({
  name: "GestionnaireGaspillageAlimentaireModifier",
  params: {
    canteenUrlComponent: props.canteenUrlComponent,
    id: displayMeasurement.value.id,
  },
}))

const activeAccordion = ref("")
</script>

<template>
  <div>
    <div v-if="displayMeasurement" class="fr-grid-row fr-grid-row--gutters">
      <div class="fr-col-12 fr-col-md-4 fr-mb-4w">
        <div v-if="editable" class="fr-grid-row fr-grid-row--bottom fr-mb-4w">
          <div class="fr-col-12 fr-pr-4w">
            <DsfrSelect v-model="chosenMeasurementIdx" label="Date de l'évaluation" :options="measurementChoices" />
          </div>
        </div>
        <div v-else class="grey-text">
          <p class="fr-mb-1w">Date de l'évaluation</p>
          <p>
            <b>
              {{
                formatDate(displayMeasurement.periodStartDate, {
                  month: "short",
                  day: "numeric",
                })
              }}
              - {{ formatDate(displayMeasurement.periodEndDate) }}
            </b>
          </p>
        </div>
        <div>
          <EmphasiseText
            :emphasisText="`${formatNumber(wastePerMeal)} g`"
            contextText="par repas et par convive"
            class="brown"
          />
        </div>
        <p v-if="editable">
          <router-link :to="measurementTunnel" class="fr-btn fr-btn--secondary fr-btn--sm fr-mr-1w fr-mb-1w">
            Modifier les données
          </router-link>
          <router-link :to="newMeasurementRoute" class="fr-btn fr-btn--primary fr-btn--sm">
            Saisir une nouvelle évaluation
          </router-link>
        </p>
      </div>
      <div
        v-if="displayMeasurement.isSortedBySource"
        class="fr-col-12 fr-col-md-8 fr-mb-4w fr-grid-row fr-grid-row--gutters"
      >
        <div class="fr-col-12 fr-col-sm-6">
          <EdibleChart :measurement="displayMeasurement" />
        </div>
        <div class="fr-col-12 fr-col-sm-6">
          <SourceChart :measurement="displayMeasurement" />
        </div>
      </div>
      <div v-else class="fr-col-12 fr-col-md-4 fr-mb-4w">
        <DsfrAlert>
          Triez vos déchets alimentaires par source pour mieux comprendre comment agir.
        </DsfrAlert>
      </div>
    </div>
    <DsfrAccordionsGroup v-model="activeAccordion">
      <DsfrAccordion id="waste-measurement-detail" title="Données détaillées" class="fr-my-2w">
        <MeasurementDetail :measurement="displayMeasurement" />
        <router-link v-if="editable" class="fr-btn fr-btn--tertiary fr-btn--sm" :to="measurementTunnel">
          <span class="fr-icon-pencil-line fr-icon--sm fr-mr-1w"></span>
          Modifier les données
        </router-link>
      </DsfrAccordion>
    </DsfrAccordionsGroup>
  </div>
</template>

<style scoped>
.grey-text {
  color: var(--text-mention-grey);
}
</style>
