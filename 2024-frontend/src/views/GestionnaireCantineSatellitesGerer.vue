<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import canteenService from "@/services/canteens.js"
import urlService from "@/services/urls.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import CanteenButtonJoin from "@/components/CanteenButtonJoin.vue"

const route = useRoute()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteen = computedAsync(async () => await canteenService.fetchCanteen(canteenId), {})
const satellites = computedAsync(async () => await canteenService.fetchSatellites(canteenId), {})

const satellitesCountSentence = computed(() => {
  if (!satellites.value.count) return ""
  const canteenSentence =
    satellites.value.count > 1 ? "cantines satellites renseignées" : "cantine satellite renseignée"
  return `${satellites.value.count} / ${canteen.value.satelliteCanteensCount} ${canteenSentence}`
})

const tableHeaders = [
  {
    key: "name",
    label: "Nom",
  },
  {
    key: "siretSiren",
    label: "SIRET ou SIREN",
  },
  {
    key: "dailyMealCount",
    label: "Couverts par jour",
  },
  {
    key: "edit",
    label: "Modifier",
  },
  {
    key: "remove",
    label: "Enlever",
  },
]

const tableRows = computed(() => {
  return !satellites.value.results
    ? []
    : satellites.value.results.map((sat) => {
        return {
          name: sat.name,
          siretSiren: sat.siret || sat.sirenUniteLegale,
          dailyMealCount: sat.dailyMealCount,
          edit: {
            userCan: sat.userCanView,
            canteenComponentUrl: sat.userCanView ? urlService.getCanteenUrl(sat) : "",
            sat: sat,
          },
          delete: "a faire",
        }
      })
})
</script>
<template>
  <section>
    <div class="fr-col-12 fr-col-md-8">
      <h1>{{ route.meta.title }}</h1>
      <p v-if="!canteen.isCentralCuisine">
        Votre établissement n'est pas une cuisine centrale, vous ne pouvez pas associer de cuisines satellites. Pour
        modifier votre type d'établissement
        <AppLinkRouter
          title="cliquez-ici"
          :to="{ name: 'GestionnaireCantineModifier', params: route.canteenUrlComponent }"
        />
      </p>
    </div>
    <div class="fr-grid-row fr-grid-row--middle fr-mb-4w" v-if="canteen.isCentralCuisine">
      <p class="fr-col-12 fr-col-md-6 fr-mb-0">
        {{ satellitesCountSentence }}
      </p>
      <div class="fr-col-12 fr-col-md-6 fr-grid-row fr-grid-row--right">
        <router-link
          :to="{
            name: 'GestionnaireCantineSatellitesAjouter',
            params: { canteenUrlComponent: route.canteenUrlComponent },
          }"
        >
          <DsfrButton label="Ajouter une cantine satellite" />
        </router-link>
      </div>
    </div>
    <DsfrDataTable
      v-if="tableRows"
      title="Vos cantines satellites"
      no-caption
      :headers-row="tableHeaders"
      :rows="tableRows"
      :sortable-rows="['name', 'siretSiren', 'dailyMealCount']"
    >
      <template #cell="{ colKey, cell }">
        <template v-if="colKey === 'edit'">
          <router-link
            v-if="cell.userCan"
            :to="{ name: 'GestionnaireCantineModifier', params: { canteenUrlComponent: cell.canteenComponentUrl } }"
            class="ma-cantine--unstyled-link"
          >
            <DsfrButton tertiary label="Modifier" />
          </router-link>
          <CanteenButtonJoin v-else :id="cell.sat.id" :name="cell.sat.name" />
        </template>
        <template v-else>
          {{ cell }}
        </template>
      </template>
    </DsfrDataTable>
  </section>
</template>
