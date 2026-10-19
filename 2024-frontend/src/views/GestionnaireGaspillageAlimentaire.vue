<script setup>
import { computed, ref, watch } from "vue"
import { useRootStore } from "@/stores/root"
import { useRouter } from "vue-router"
import { formatNumber } from "@/utils"
import urlService from "@/services/urls"
import WasteMeasurementSummary from "@/components/WasteMeasurementSummary.vue"
import EmphasiseText from "@/components/EmphasiseText.vue"
import AppLinkMailto from "@/components/AppLinkMailto.vue"

const props = defineProps(["canteenUrlComponent"])
const store = useRootStore()
const router = useRouter()

const canteenId = computed(() => props.canteenUrlComponent ? +props.canteenUrlComponent.split("--")[0] : null)
const canteen = computed(() => store.canteenPreviews.find((canteen) => canteen.id === canteenId.value))

/* Selector */
const canteenOptions = computed(() =>
  store.canteenPreviews
    .map((canteen) => ({ value: canteen.id, text: canteen.name }))
    .sort((a, b) => a.text.localeCompare(b.text))
)

const selectCanteen = (id) => {
  const selectedCanteen = store.canteenPreviews.find((canteen) => canteen.id === Number(id))
  if (!selectedCanteen) return
  router.push({
    name: "GestionnaireGaspillageAlimentaire",
    params: { canteenUrlComponent: urlService.getCanteenUrl(selectedCanteen) },
  })
}

/* Redirect */
const newMeasurementRoute = computed(() => ({
  name: "GestionnaireGaspillageAlimentaireModifier",
  params: { canteenUrlComponent: props.canteenUrlComponent },
}))

/* Measurements */
const measurements = ref([])

watch(
  canteenId,
  (id) => {
    measurements.value = []
    if (!id) return
    fetch(`/api/v1/canteens/${id}/wasteMeasurements`)
      .then((response) => response.json())
      .then((response) => {
        measurements.value = response
      })
  },
  { immediate: true }
)
</script>

<template>
  <div>
    <DsfrAlert title="Cette page va bientôt évoluer" type="info" class="fr-mb-4w">
      <p>
        Une nouvelle version de la page de suivi des déchets alimentaires sera bientôt disponible, construite à partir
        de vos retours dans un souci de simplicité et de performance.
      </p>
      <p>Pour toute remarque ou question : <AppLinkMailto /></p>
    </DsfrAlert>
    <h1>Déchets alimentaires</h1>
    <DsfrSelect
      :modelValue="canteen?.id"
      @update:modelValue="selectCanteen"
      label="Pour l'établissement :"
      :options="canteenOptions"
      defaultUnselectedText="Sélectionnez une cantine ou un groupe de cantines"
      class="fr-mb-4w"
    />
    <template v-if="canteen">
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
          Votre établissement est soumis à l'obligation de faire une analyse des causes des déchets alimentaires, et
          de mettre en place une démarche de lutte contre les déchets alimentaires.
        </p>
        <DsfrBadge label="Pas encore de données" type="none" />
        <EmphasiseText :emphasisText="`${formatNumber()} g`" contextText="par repas et par convive" />
        <router-link :to="newMeasurementRoute" class="fr-btn">
          Saisir une évaluation
        </router-link>
      </div>
    </template>
  </div>
</template>

<style scoped>
.fr-grid-row--center {
  align-items: center;
}
</style>
