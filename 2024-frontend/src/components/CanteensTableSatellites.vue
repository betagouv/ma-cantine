<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import diagnosticService from "@/services/diagnostics.js"
import campaignService from "@/services/campaigns.js"
import urlService from "@/services/urls.js"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"

const props = defineProps(["satellites", "groupe"])
const lastYear = new Date().getFullYear() - 1

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
    key: "actions",
    label: "Actions",
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
            isManagedByUser: sat.isManagedByUser,
          },
          siretSiren: sat.siret || sat.sirenUniteLegale,
          dailyMealCount: sat.dailyMealCount,
          diagnostic: diagnosticService.getBadge(sat.action, campaign.value),
          actions: getSatelliteActions(sat),
        }
      })
})

const getSatelliteActions = (sat) => {
  const actions = []
  switch (true) {
    case sat.isManagedByUser:
      actions.push({
        label: "Modifier",
        to: { name: 'GestionnaireCantineRestaurantModifier', params: { canteenUrlComponent: sat.userCanView ? urlService.getCanteenUrl(sat) : "" } },
      })
      break
    case sat.canBeClaimed:
      actions.push({
        label: "Revendiquer la cantine",
        emitEvent: 'claimCanteen',
      })
      break
    case !sat.isManagedByUser && !sat.canBeClaimed:
      actions.push({
        label: "Demander à rejoindre",
        emitEvent: 'removeSatellite',
      })
      break
  }

  actions.push({
    label: "Retirer de mon groupe",
    emitEvent: 'removeSatellite',
  })

  return actions
}
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
            v-if="cell.isManagedByUser"
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
      <template v-else-if="colKey === 'actions'">
        <div class="fr-grid-row fr-grid-row--right">
          <AppDropdownMenu label="Actions" :links="cell" size="small" />
        </div>
      </template>
      <template v-else>
        {{ cell }}
      </template>
    </template>
  </DsfrDataTable>
</template>
