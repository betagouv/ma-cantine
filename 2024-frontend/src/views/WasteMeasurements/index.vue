<script setup>
import { computed, onMounted, ref } from "vue"
import { useRootStore } from "@/stores/root"
import { useRouter } from "vue-router"
import { formatNumber } from "@/utils"
import WasteMeasurementSummary from "@/components/WasteMeasurementSummary.vue"
import EmphasiseText from "@/components/EmphasiseText.vue"

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

const measurements = ref([])

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
    <h1>Déchets alimentaires</h1>
    <p>
      {{ canteen.name }}&nbsp;
      <router-link :to="{ name: 'ManagementPage' }" class="fr-btn fr-btn--tertiary fr-btn--sm">
        Changer d'établissement
      </router-link>
    </p>
    <h2>Mes déchets alimentaires mesurés</h2>
    <div v-if="measurements.length">
      <WasteMeasurementSummary
        :measurements="measurements"
        :editable="true"
        :canteenUrlComponent="canteenUrlComponent"
      />
    </div>
    <div v-else>
      <p>
        Votre établissement est soumis à l'obligation de faire une analyse des causes des déchets alimentaires, et de
        mettre en place une démarche de lutte contre les déchets alimentaires.
      </p>
      <DsfrBadge label="Pas encore de données" type="none" />
      <EmphasiseText :emphasisText="`${formatNumber()} g`" contextText="par repas et par convive" />
      <router-link :to="newMeasurementRoute" class="fr-btn">
        Saisir une évaluation
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.fr-grid-row--center {
  align-items: center;
}
</style>
