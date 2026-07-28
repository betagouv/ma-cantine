<script setup>
import { computed, ref } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import canteenService from "@/services/canteens.js"
import canteensTableService from "@/services/canteensTable.js"
import urlService from "@/services/urls.js"
import AppLoader from "@/components/AppLoader.vue"
import LayoutSidebarCanteen from "@/layouts/LayoutSidebarCanteen.vue"
import CanteensTableSatellites from "@/components/CanteensTableSatellites.vue"
import CanteenModalSatelliteAdd from "@/components/CanteenModalSatelliteAdd.vue"
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
const satellitesDisplayed = computed(() => isSearching.value ? canteensTableService.searchCanteensBySiretOrSirenOrName(search.value, satellites.value) : satellites.value)

const updateSatellites = () => {
  loading.value = true
  canteenService.fetchSatellites(canteenId).then((response) => {
    loading.value = false
    satellites.value = response
  })
}
updateSatellites()

const satellitesCountSentence = computed(() => {
  const number = getSatellitesPrettCount(satellitesDisplayed.value.length)
  const type = getSatellitesPrettyType(satellitesDisplayed.value.length)
  return `${number} ${type}`
})

const getSatellitesPrettCount = (count) => {
  if (count === 0) return "Aucun restaurant satellite"
  else if (count === 1) return "1 restaurant satellite"
  else return `${count} restaurants satellites`
}

const getSatellitesPrettyType = (count) => {
  if (isSearching.value && count <= 1 ) return `trouvé pour la recherche « ${search.value} »`
  if (isSearching.value && count > 1 ) return `trouvés pour la recherche « ${search.value} »`
  if (!isSearching.value && count <= 1) return "renseigné"
  if (!isSearching.value && count > 1) return "renseignés"
}

const removeSatellite = (id) => {
  satellites.value = satellites.value.filter((sat) => sat.id !== id)
}

const showModalRemoveSatellite = (satellite) => {
  satelliteToRemove.value = satellite
  modalRemoveSatelliteOpened.value = true
}

/* Search */
const search = ref()
const isSearching = ref(false)

const updateSearch = () => {
  if(search.value.trim() === "") isSearching.value = false
}

const clickSearch = () => {
  isSearching.value = true
}
</script>
<template>
  <LayoutSidebarCanteen class="gestionnaire-cantine-groupe" :title="route.meta.title">
    <template #titleName>{{ route.meta.title }}</template>
    <template #titleButton>
      <DsfrButton primary label="Ajouter une cantine au groupe" icon="fr-icon-add-circle-fill" @click="modalAddSatelliteOpened = true" />
    </template>
    <template #content>
      <AppLoader v-if="loading" />
      <div class="fr-grid-row fr-mb-2w fr-grid-row--middle">
        <div class="fr-col-12 fr-col-md-6">
          <p class="fr-mb-md-0">{{ satellitesCountSentence }}</p>
        </div>
        <div class="fr-col-12 fr-col-md-6">
          <DsfrSearchBar
            v-model="search"
            label="Rechercher"
            button-text="Rechercher"
            placeholder="Rechercher par le nom, siret ou siren de l'établissement"
            @update:modelValue="updateSearch"
            @search="clickSearch"
          />
        </div>
      </div>
      <CanteensTableSatellites
        v-if="satellitesDisplayed.length > 0"
        :satellites="satellitesDisplayed"
        :groupe="canteen"
        @updateSatellites="updateSatellites"
        @showModalRemoveSatellite="showModalRemoveSatellite" />
      <CanteenModalSatelliteAdd
        :open="modalAddSatelliteOpened"
        :groupId="canteenId"
        @close="modalAddSatelliteOpened = false"
        @updateSatellites="updateSatellites()" />
      <CanteenModalSatelliteRemove
        v-if="satelliteToRemove"
        :opened="modalRemoveSatelliteOpened"
        :groupe="canteen"
        :satellite="satelliteToRemove"
        @close="modalRemoveSatelliteOpened = false"
        @satelliteRemoved="removeSatellite(satelliteToRemove.id)"
      />
    </template>
  </LayoutSidebarCanteen>

</template>

<style lang="scss">
.gestionnaire-cantine-groupe {
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
