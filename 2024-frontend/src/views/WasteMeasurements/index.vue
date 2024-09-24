<script setup>
import { computed, onMounted, ref } from "vue"
import { useRootStore } from "@/stores/root"
import { useRouter } from "vue-router"
import { formatNumber, formatDate } from "@/utils"
import MeasurementDetail from "./MeasurementDetail.vue"
import SourceChart from "./SourceChart.vue"

const props = defineProps(["canteenUrlComponent"])
const store = useRootStore()
const router = useRouter()

const canteenId = computed(() => +props.canteenUrlComponent.split("--")[0])
const canteen = computed(() => {
  const canteen = store.canteenPreviews.find((canteen) => canteen.id === canteenId.value)
  if (!canteen) router.replace({ name: "ManagementPage" })
  return {
    id: canteenId,
    name: canteen?.name,
  }
})

const newMeasurementRoute = {
  name: "WasteMeasurementTunnel",
  params: { canteenUrlComponent: props.canteenUrlComponent },
}

const measurementTunnel = computed(() => ({
  name: "WasteMeasurementTunnel",
  params: {
    canteenUrlComponent: props.canteenUrlComponent,
    id: measurement.value.id,
  },
}))

const measurements = ref([])
const chosenMeasurementIdx = ref(0)
const measurement = computed(() => measurements.value.length && measurements.value[chosenMeasurementIdx.value])
const measurementChoices = computed(() => {
  return measurements.value.map((m, idx) => {
    return {
      text: `${formatDate(m.periodStartDate, {
        month: "short",
        day: "numeric",
      })} - ${formatDate(m.periodEndDate)}`,
      value: idx,
    }
  })
})

const wastePerMeal = computed(() => {
  const m = measurement.value
  if (m && m.totalMass && m.mealCount) return (m.totalMass / m.mealCount) * 1000 // convert kg to g
  return undefined
})

const activeAccordion = ref("")

onMounted(() => {
  fetch(`/api/v1/canteens/${canteenId.value}/wasteMeasurements`)
    .then((response) => response.json())
    .then((response) => {
      measurements.value = response
    })
})
</script>

<template>
  <div>
    <h1>Gaspillage alimentaire</h1>
    <p>
      {{ canteen.name }}&nbsp;
      <router-link :to="{ name: 'ManagementPage' }" class="fr-btn fr-btn--tertiary fr-btn--sm">
        Changer d'établissement
      </router-link>
    </p>
    <h2>Mon gaspillage mesuré</h2>
    <div v-if="measurements.length">
      <div v-if="measurement" class="fr-grid-row fr-grid-row--center">
        <div class="fr-col fr-mb-4w">
          <p class="highlight brown">
            <span class="fr-h3">{{ formatNumber(wastePerMeal) }} g</span>
            par repas
          </p>
          <router-link :to="newMeasurementRoute" class="fr-btn fr-btn--secondary fr-mt-sm-2w">
            Saisir une nouvelle évaluation
          </router-link>
        </div>
        <div class="fr-col-12 fr-col-sm-5 fr-mb-4w">
          <div v-if="measurement.isSortedBySource">
            <SourceChart :measurement="measurement" />
          </div>
          <div v-else>
            <DsfrAlert>
              Triez votre gaspillage alimentaire par source pour mieux comprendre comment agir.
            </DsfrAlert>
          </div>
        </div>
      </div>
      <DsfrAccordionsGroup v-model="activeAccordion">
        <DsfrAccordion id="waste-measurement-detail" title="Données détaillées" class="fr-my-2w">
          <div class="fr-grid-row fr-grid-row--bottom fr-mb-4w">
            <div class="fr-col-12 fr-col-sm-6 fr-col-md-4 fr-pr-4w">
              <DsfrSelect v-model="chosenMeasurementIdx" label="Date de l'évaluation" :options="measurementChoices" />
            </div>
            <div class="fr-col-12 fr-col-sm-4">
              <router-link class="fr-btn fr-btn--tertiary" :to="measurementTunnel">
                <span class="fr-icon-pencil-line fr-icon--sm fr-mr-1w"></span>
                Modifier les données
              </router-link>
            </div>
          </div>
          <MeasurementDetail :measurement="measurement" />
          <router-link class="fr-btn fr-btn--tertiary fr-btn--sm" :to="measurementTunnel">
            <span class="fr-icon-pencil-line fr-icon--sm fr-mr-1w"></span>
            Modifier les données
          </router-link>
        </DsfrAccordion>
      </DsfrAccordionsGroup>
    </div>
    <div v-else>
      <p>
        Votre établissement est soumis à l'obligation de faire une analyse des causes du gaspillage alimentaire, et de
        mettre en place une démarche de lutte contre le gaspillage alimentaire.
      </p>
      <DsfrBadge label="Pas encore des données" type="none" />
      <p class="fr-my-4w highlight">
        <span class="fr-h3">{{ formatNumber() }} g</span>
        par repas
      </p>
      <router-link :to="newMeasurementRoute" class="fr-btn">
        Saisir une évaluation
      </router-link>
    </div>
  </div>
</template>

<style scoped>
p.highlight {
  color: var(--text-mention-grey);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
p.highlight > span {
  border-radius: 18px;
  padding: 4px 16px;
  margin-right: 8px;
  margin-bottom: 0;

  background: var(--background-default-grey-hover);
  color: inherit;
}
p.highlight.brown {
  color: var(--text-action-high-orange-terre-battue);
}
p.highlight.brown > span {
  background: var(--orange-terre-battue-975-75);
}

.fr-grid-row--center {
  align-items: center;
}
</style>
