<script setup>
import { computed } from "vue"
import diagnosticService from "@/services/diagnostics.js"
import urlService from "@/services/urls.js"
import cantines from "@/data/cantines.json"
import AppRawHTML from "@/components/AppRawHTML.vue"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"

const props = defineProps(["canteens", "campaign"])
const lastYear = new Date().getFullYear() - 1
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
    key: "diagnostic",
    label: `Bilan ${lastYear}`,
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
    const diagnostic = getDiagnosticInfos(canteen)
    const actions = getActionsInfos(canteen)

    rows.push({
      name,
      siret,
      city,
      productionType,
      diagnostic,
      actions,
    })
  })
  return rows
})

const getNameInfos = (canteen) => {
  const satellitesCount = 2 // TODO : get value from canteen
  const satellitesCountSentence = satellitesCount !== "" ? getSatellitesCountSentence(satellitesCount) : null
  return {
    name: canteen.name,
    url: urlService.getCanteenUrl(canteen),
    satellitesCountSentence,
  }
}

const getSatellitesCountSentence = (satellitesCount) => {
  const number = satellitesCount === 0 ? "Aucun" : satellitesCount
  const name = satellitesCount <= 1 ? "restaurant satellite" : "restaurants satellites"
  return `${number} ${name}`
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

const getDiagnosticInfos = (canteen) => {
  const action = canteen.action
  const badge = diagnosticService.getBadge(action, props.campaign)
  const button = getTeledeclareButton(canteen)
  return { badge, button }
}

const getActionsInfos = (canteen) => {
  const dropdownLinks = getDropdownLinks(canteen)
  return dropdownLinks
}

const getDropdownLinks = (canteen) => {
  const canteenUrlComponent = urlService.getCanteenUrl(canteen)
  const links = [
    {
      label: "Modifier l'établissement",
      to: { name: "GestionnaireCantineGerer", params: { canteenUrlComponent: canteenUrlComponent } },
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

  if (canteen.productionType === "central" || canteen.productionType === "central_serving" || canteen.productionType === "groupe") {
    links.push({
      to: { name: "GestionnaireCantineGroupeGerer", params: { canteenUrlComponent: canteenUrlComponent } },
      label: "Gérer les restaurants satellites",
    })
  }
  return links
}

const getTeledeclareButton = (canteen) => {
  const button = diagnosticService.getTeledeclareButton(canteen.action)
  if (!button) return false
  const canteenUrlComponent = urlService.getCanteenUrl(canteen)
  return { ...button, canteenUrlComponent, year: lastYear }
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
            <p v-if="cell.satellitesCountSentence" class="fr-text-title--blue-france fr-mb-0 fr-text--sm">
              <VIcon name="ri-node-tree" class="fr-pb-0-5v" />
              {{ cell.satellitesCountSentence }}
            </p>
          </template>
          <template v-else-if="colKey === 'diagnostic'">
            <router-link
              v-if="cell.button"
              :to="{
                name: cell.button.name,
                params: {
                  year: cell.button.year,
                  canteenUrlComponent: cell.button.canteenUrlComponent,
                  measureId: cell.button.measure,
                },
              }"
              class="ma-cantine--unstyled-link"
            >
              <DsfrButton
                v-if="cell.button"
                :label="cell.button.label"
                :icon="cell.button.icon"
                size="small"
                class="fr-mr-1v"
              />
            </router-link>
            <DsfrBadge v-else small :label="cell.badge.label" :type="cell.badge.type" no-icon />
          </template>
          <template v-else-if="colKey === 'actions'">
            <div class="fr-grid-row fr-grid-row--right">
              <AppDropdownMenu label="Paramètres" icon="fr-icon-settings-5-line" :links="cell" size="small" />
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

  th:nth-child(1) {
    width: 35% !important;
  }

  td:nth-child(1),
  td:nth-child(4) {
    white-space: pre-wrap !important;
  }
}
</style>
