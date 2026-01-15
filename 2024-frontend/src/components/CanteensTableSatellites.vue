<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import diagnosticService from "@/services/diagnostics.js"
import campaignService from "@/services/campaigns.js"
import urlService from "@/services/urls.js"
import CanteenButtonJoin from "@/components/CanteenButtonJoin.vue"
import CanteenButtonUnlink from "@/components/CanteenButtonUnlink.vue"

const props = defineProps(["satellites", "groupe"])
const lastYear = new Date().getFullYear() - 1
const emit = defineEmits(["removeSatellite"])

/* Campaign */
const campaign = computedAsync(async () => {
  return await campaignService.getYearCampaignDates(lastYear)
}, false)


/* Table */
const tableHeaders = [
  {
    key: "name",
    label: "Nom",
  },
  {
    key: "siretSiren",
    label: "SIRET / SIREN",
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
  return !props.satellites
    ? []
    : props.satellites.map((sat) => {
        return {
          name: {
            canteen: sat.name,
            url: urlService.getCanteenUrl(sat),
            isManager: sat.userCanView,
          },
          siretSiren: sat.siret || sat.sirenUniteLegale,
          dailyMealCount: sat.dailyMealCount,
          diagnostic: diagnosticService.getBadge(sat.action, campaign.value),
          edit: {
            userCan: sat.userCanView,
            satelliteComponentUrl: sat.userCanView ? urlService.getCanteenUrl(sat) : "",
            satellite: sat,
          },
          remove: {
            satellite: sat,
            groupe: props.groupe,
          },
        }
      })
})
</script>

<template>
  <DsfrDataTable
    title="Vos restaurants satellites"
    no-caption
    :headers-row="tableHeaders"
    :rows="tableRows"
    :sortable-rows="['name', 'diagnostic']"
    :pagination="true"
    :pagination-options="[50, 100, 200]"
    :rows-per-page="50"
    pagination-wrapper-class="fr-mt-3w"
    class="gestionnaire-cantine-groupe-satellites__table"
  >
    <template #cell="{ colKey, cell }">
      <template v-if="colKey === 'name'">
        <p class="fr-text-title--blue-france fr-text--bold">
          <router-link
            v-if="cell.isManager"
            :to="{ name: 'DashboardManager', params: { canteenUrlComponent: cell.url } }"
          >
            {{ cell.canteen }}
          </router-link>
          <span v-else>
            {{ cell.canteen }}
          </span>
        </p>
      </template>
      <template v-else-if="colKey === 'diagnostic'">
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
          :groupe="cell.groupe"
          :satellite="cell.satellite"
          @satelliteRemoved="emit('removeSatellite', cell.satellite.id)"
        />
      </template>
      <template v-else>
        {{ cell }}
      </template>
    </template>
  </DsfrDataTable>
</template>
