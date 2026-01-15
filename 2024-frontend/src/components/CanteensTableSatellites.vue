<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import diagnosticService from "@/services/diagnostics.js"
import campaignService from "@/services/campaigns.js"
import canteensService from "@/services/canteens"
import urlService from "@/services/urls.js"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"

/* Settings */
const props = defineProps(["satellites", "groupe"])
const emit = defineEmits(["showModalRemoveSatellite"])
const lastYear = new Date().getFullYear() - 1
const store = useRootStore()

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
          actions: {
            links: getActions(sat),
            canteen: sat,
          },
        }
      })
})

/* Actions */
const getActions = (sat) => {
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
        emitEvent: 'joinCanteen',
      })
      break
  }

  actions.push({
    label: "Retirer de mon groupe",
    emitEvent: 'showModalRemoveSatellite',
  })

  return actions
}

const clickAction = (emitEvent, canteen) => {
  if (emitEvent === 'joinCanteen') joinCanteen(canteen)
  else if (emitEvent === 'showModalRemoveSatellite') emit('showModalRemoveSatellite', canteen)
}

const joinCanteen = (canteen) => {
  const userInfos = {
    email: store.loggedUser.email,
    name: `${store.loggedUser.firstName} ${store.loggedUser.lastName}`,
  }
  canteensService
    .teamJoinRequest(canteen.id, userInfos)
    .then(() => {
      store.notify({
        title: "Demande envoyée",
        message: `Nous avons contacté l'équipe de la cantine ${canteen.name}. Ces derniers reviendront vers vous pour accepter ou non votre demande.`,
      })
    })
    .catch(store.notifyServerError)
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
          <AppDropdownMenu label="Actions" :links="cell.links" size="small" @click="(event) => clickAction(event, cell.canteen)" />
        </div>
      </template>
      <template v-else>
        {{ cell }}
      </template>
    </template>
  </DsfrDataTable>
</template>
