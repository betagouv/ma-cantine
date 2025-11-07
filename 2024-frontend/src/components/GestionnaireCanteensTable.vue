<script setup>
import { computed } from "vue"
import actionService from "@/services/actions.js"
import urlService from "@/services/urls.js"
import cantines from "@/data/cantines.json"
import AppRawHTML from "@/components/AppRawHTML.vue"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"

const props = defineProps(["canteens"])

const header = [
  {
    key: "name",
    label: "Nom de la cantine",
  },
  {
    key: "siret",
    label: "Siret / Siren",
  },
  {
    key: "city",
    label: "Commune </br> (code postal)",
  },
  { key: "productionType", label: "Type" },
  {
    key: "status",
    label: "Statut",
  },
  {
    key: "actions",
    label: "Actions",
  },
]

const rows = computed(() => {
  const rows = []
  props.canteens.forEach((canteen) => {
    const name = getNameInfos(canteen)
    const siret = getSiretOrSirenInfos(canteen)
    const city = getCityInfos(canteen)
    const productionType = getProductionTypeInfos(canteen)
    const status = getStatusInfos(canteen)
    const actions = getActionsInfos(canteen)

    rows.push({
      name,
      siret,
      city,
      productionType,
      status,
      actions,
    })
  })
  return rows
})

const getNameInfos = (canteen) => {
  return {
    name: canteen.name,
    url: urlService.getCanteenUrl(canteen),
  }
}

const getSiretOrSirenInfos = (canteen) => {
  return canteen.siret || canteen.sirenUniteLegale
}

const getCityInfos = (canteen) => {
  let city = ""
  if (canteen.city) city += canteen.city
  if (canteen.postalCode) city += ` (${canteen.postalCode})`
  if (!canteen.city && !canteen.postalCode) city = "Non renseigné"
  return city
}

const getProductionTypeInfos = (canteen) => {
  const slug = canteen.productionType
  const index = cantines.productionType.findIndex((type) => type.value === slug)
  return cantines.productionType[index].label
}

const getStatusInfos = (canteen) => {
  const action = canteen.action
  const badge = actionService.getBadge(action)
  return {
    label: badge.body,
    type: badge.mode,
  }
}

const getActionsInfos = (canteen) => {
  const dropdownLinks = getDropdownLinks(canteen)
  const quickAction = getQuickAction(canteen)
  return { dropdownLinks, quickAction }
}

const getDropdownLinks = (canteen) => {
  const canteenUrlComponent = urlService.getCanteenUrl(canteen)
  const links = [
    {
      label: "Modifier la cantine",
      to: { name: "DashboardManager", params: { canteenUrlComponent: canteenUrlComponent } },
    },
    {
      label: "Ajouter des achats",
      to: { name: "PurchasesHome" },
    },
    {
      label: "Gérer les collaborateurs",
      to: { name: "CanteenManagers", params: { canteenUrlComponent: canteenUrlComponent } },
    },
  ]

  if (canteen.productionType === "central" || canteen.productionType === "central_serving") {
    links.push({
      to: { name: "GestionnaireCantineSatellitesGerer", params: { canteenUrlComponent: canteenUrlComponent } },
      label: "Gérer les satellites",
    })
  }
  return links
}

const getQuickAction = (canteen) => {
  const button = actionService.getButton(canteen.action)
  if (!button) return false
  const canteenUrlComponent = urlService.getCanteenUrl(canteen)
  const year = new Date().getFullYear() - 1
  return { ...button, canteenUrlComponent, year }
}
</script>
<template>
  <div class="gestionnaire-canteens-table">
    <div class="gestionnaire-canteens-table__scrollable">
      <DsfrDataTable
        class="gestionnaire-canteens-table__content"
        title="Vos cantines"
        no-caption
        :headers-row="header"
        :rows="rows"
        :pagination="true"
        :pagination-options="[50, 100, 200]"
        :rows-per-page="50"
        pagination-wrapper-class="fr-mt-2w"
      >
        <template #header="{ label }">
          <AppRawHTML :html="label" />
        </template>
        <template #cell="{ colKey, cell }">
          <template v-if="colKey === 'name'">
            <p>
              <router-link
                :to="{ name: 'DashboardManager', params: { canteenUrlComponent: cell.url } }"
                class="fr-text-title--blue-france fr-text--bold"
              >
                {{ cell.name }}
              </router-link>
            </p>
          </template>
          <template v-else-if="colKey === 'status'">
            <DsfrBadge small :label="cell.label" :type="cell.type" />
          </template>
          <template v-else-if="colKey === 'actions'">
            <div class="fr-grid-row fr-grid-row--right">
              <router-link
                :to="{
                  name: cell.quickAction.name,
                  params: {
                    year: cell.quickAction.year,
                    canteenUrlComponent: cell.quickAction.canteenUrlComponent,
                    measureId: cell.quickAction.measure,
                  },
                }"
                class="ma-cantine--unstyled-link"
              >
                <DsfrButton
                  v-if="cell.quickAction"
                  :label="cell.quickAction.label"
                  :icon="cell.quickAction.icon"
                  size="small"
                  class="fr-mr-1v"
                />
              </router-link>
              <AppDropdownMenu
                label="Paramètres"
                icon="fr-icon-settings-5-line"
                :links="cell.dropdownLinks"
                size="small"
              />
            </div>
          </template>
          <template v-else>
            <p class="fr-text--xs">{{ cell }}</p>
          </template>
        </template>
      </DsfrDataTable>
    </div>
  </div>
</template>

<style lang="scss">
.gestionnaire-canteens-table {
  overflow-x: hidden;

  &__scrollable {
    overflow: scroll;
  }

  &__content {
    min-width: 75rem; // Calculated from fr-container { max-width 78rem, padding-left: 1.5rem, padding-right: 1.5rem }
  }

  .fr-table__container {
    overflow: initial !important;
  }

  th,
  td {
    white-space: initial !important;
    word-break: break-word;
  }

  th:nth-child(1) {
    width: 20% !important;
  }

  th:nth-child(2) {
    width: 10% !important;
  }

  td:nth-child(2) {
    padding-right: 0% !important;
  }

  td:last-child {
    padding-left: 0 !important;
  }

  th:nth-child(3) {
    width: 15% !important;
  }

  th:nth-child(4) {
    width: 10% !important;
  }

  th:nth-child(5) {
    width: 20% !important;
  }

  th:nth-child(6) {
    width: 25% !important;
  }
}
</style>
