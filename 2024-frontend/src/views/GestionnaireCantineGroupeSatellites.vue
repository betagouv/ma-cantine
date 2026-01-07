<script setup>
import { computed, ref } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import canteenService from "@/services/canteens.js"
import diagnosticService from "@/services/diagnostics.js"
import campaignService from "@/services/campaigns.js"
import urlService from "@/services/urls.js"
import AppLoader from "@/components/AppLoader.vue"
import CanteenButtonJoin from "@/components/CanteenButtonJoin.vue"
import CanteenButtonUnlink from "@/components/CanteenButtonUnlink.vue"

const route = useRoute()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteen = computedAsync(async () => await canteenService.fetchCanteen(canteenId), {})
const loading = ref(true)

/* CAMPAIGN */
const campaign = computedAsync(async () => {
  const lastYear = new Date().getFullYear() - 1
  return await campaignService.getYearCampaignDates(lastYear)
}, false)

/* Satellites  */
const satellites = ref([])
canteenService.fetchSatellites(canteenId).then((response) => {
  loading.value = false
  satellites.value = response
})

const satellitesCountSentence = computed(() => {
  if (satellites.value.length === 0) return "Aucun restaurant satellite renseigné"
  else if (satellites.value.length === 1) return "1 restaurant satellite renseigné"
  else return `${satellites.value.length} restaurants satellites renseignés`
})

/* Table */
const lastYear = new Date().getFullYear() - 1
const tableHeaders = [
  {
    key: "name",
    label: "Nom",
  },
  {
    key: "siretSiren",
    label: "Siret / Siren",
  },
  {
    key: "dailyMealCount",
    label: "Couverts par jour",
  },
  {
    key: "diagnostic",
    label: `Bilan ${lastYear}`,
  },
  {
    key: "edit",
    label: "Modifier",
  },
  {
    key: "remove",
    label: "Retirer",
  },
]

const tableRows = computed(() => {
  return !satellites.value
    ? []
    : satellites.value.map((sat) => {
        return {
          name: sat.name,
          siretSiren: sat.siret || sat.sirenUniteLegale,
          dailyMealCount: sat.dailyMealCount,
          diagnostic: diagnosticService.getBadge(sat.action, campaign),
          edit: {
            userCan: sat.userCanView,
            satelliteComponentUrl: sat.userCanView ? urlService.getCanteenUrl(sat) : "",
            satellite: sat,
          },
          remove: {
            satellite: sat,
            canteen: canteen.value,
          },
        }
      })
})

/* Rows */
const removeRow = (id) => {
  satellites.value = satellites.value.filter((sat) => sat.id !== id)
}
</script>
<template>
  <section class="gestionnaire-cantine-groupe-satellites">
    <h1 class="fr-col-12 fr-col-md-7">{{ route.meta.title }}</h1>
    <div class="fr-grid-row fr-grid-row--middle fr-mb-2w">
      <p class="fr-col-12 fr-col-md-4 fr-mb-md-0">{{ satellitesCountSentence }}</p>
      <div class="fr-col-12 fr-col-md-8 fr-grid-row fr-grid-row--right">
      </div>
    </div>
    <AppLoader v-if="loading" />
    <DsfrDataTable
      v-if="tableRows.length > 0"
      title="Vos restaurants satellites"
      no-caption
      :headers-row="tableHeaders"
      :rows="tableRows"
      :sortable-rows="['name', 'siretSiren', 'dailyMealCount']"
      :pagination="true"
      :pagination-options="[50, 100, 200]"
      :rows-per-page="50"
      pagination-wrapper-class="fr-mt-3w"
      class="gestionnaire-cantine-groupe-satellites__table"
    >
      <template #cell="{ colKey, cell }">
        <template v-if="colKey === 'diagnostic'">
          <DsfrBadge small :label="cell.label" :type="cell.type" no-icon />
        </template>
        <template v-else-if="colKey === 'edit'">
          <router-link
            v-if="cell.userCan"
            :to="{ name: 'GestionnaireCantineRestaurantModifier', params: { canteenUrlComponent: cell.satelliteComponentUrl } }"
            class="ma-cantine--unstyled-link"
          >
            <DsfrButton tertiary label="Modifier" icon="fr-icon-pencil-fill" />
          </router-link>
          <CanteenButtonJoin v-else :id="cell.satellite.id" :name="cell.satellite.name" />
        </template>
        <template v-else-if="colKey === 'remove'">
          <CanteenButtonUnlink
            :canteen="cell.canteen"
            :satellite="cell.satellite"
            @satelliteRemoved="removeRow(cell.satellite.id)"
          />
        </template>
        <template v-else>
          {{ cell }}
        </template>
      </template>
    </DsfrDataTable>
  </section>
</template>

<style lang="scss">
.gestionnaire-cantine-groupe-satellites {
  &__table {
    .fr-select {
      width: 10rem !important;
    }
  }
}
</style>
