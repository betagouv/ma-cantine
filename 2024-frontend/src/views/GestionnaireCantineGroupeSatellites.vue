<script setup>
import { computed, ref } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import canteenService from "@/services/canteens.js"
import urlService from "@/services/urls.js"
import AppLoader from "@/components/AppLoader.vue"
import CanteenModalSatelliteAdd from "@/components/CanteenModalSatelliteAdd.vue"
import CanteensTableSatellites from "@/components/CanteensTableSatellites.vue"
import CanteenModalSatelliteRemove from "@/components/CanteenModalSatelliteRemove.vue"

/* Data */
const route = useRoute()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteen = computedAsync(async () => await canteenService.fetchCanteen(canteenId), {})
const loading = ref(true)
const modalAddSatelliteOpened = ref(false)
const modalRemoveSatelliteOpened = ref(false)
const satelliteToRemove = ref()

/* Satellites  */
const satellites = ref([])
const updateSatellites = () => {
  loading.value = true
  canteenService.fetchSatellites(canteenId).then((response) => {
    loading.value = false
    satellites.value = response
  })
}
updateSatellites()

const satellitesCountSentence = computed(() => {
  if (satellites.value.length === 0) return "Aucun restaurant satellite renseigné"
  else if (satellites.value.length === 1) return "1 restaurant satellite renseigné"
  else return `${satellites.value.length} restaurants satellites renseignés`
})

const removeSatellite = (id) => {
  satellites.value = satellites.value.filter((sat) => sat.id !== id)
}

const showModalRemoveSatellite = (satellite) => {
  satelliteToRemove.value = satellite
  modalRemoveSatelliteOpened.value = true
}
</script>
<template>
  <section class="gestionnaire-cantine-groupe-satellites">
    <h1 class="fr-col-12 fr-col-md-7">{{ route.meta.title }}<br/> de {{ canteen.name }}</h1>
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <p class="fr-col-12 fr-col-md-4 fr-mb-md-0">{{ satellitesCountSentence }}</p>
      <div class="fr-col-12 fr-col-md-8 fr-grid-row fr-grid-row--right">
        <DsfrButton primary label="Ajouter un restaurant satellite" icon="fr-icon-add-circle-fill" @click="modalAddSatelliteOpened = true" />
      </div>
      <CanteenModalSatelliteAdd :open="modalAddSatelliteOpened" :groupId="canteenId" @close="modalAddSatelliteOpened = false" @updateSatellites="updateSatellites()" />
    </div>
    <AppLoader v-if="loading" />
    <CanteensTableSatellites
      v-if="satellites.length > 0"
      :satellites="satellites"
      :groupe="canteen"
      @updateSatellites="updateSatellites"
      @showModalRemoveSatellite="showModalRemoveSatellite" />
    <CanteenModalSatelliteRemove
      v-if="satelliteToRemove"
      :opened="modalRemoveSatelliteOpened"
      :groupe="canteen"
      :satellite="satelliteToRemove"
      @close="modalRemoveSatelliteOpened = false"
      @satelliteRemoved="removeSatellite(satelliteToRemove.id)"
    />
  </section>
</template>

<style lang="scss">
.gestionnaire-cantine-groupe-satellites {
  &__table {
    .fr-select {
      width: 10rem !important;
    }

    tr td:first-child {
      white-space: normal !important;
    }
  }
}
</style>
