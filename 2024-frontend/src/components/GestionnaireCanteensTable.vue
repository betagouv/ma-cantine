<script setup>
import { computed } from "vue"
import urlService from "@/services/urls.js"
import canteensTableService from "@/services/canteensTable.js"
import AppRawHTML from "@/components/AppRawHTML.vue"
import AppDropdownMenu from "@/components/AppDropdownMenu.vue"
import LayoutBigTable from "@/layouts/LayoutBigTable.vue"

const props = defineProps(["canteens", "campaign"])
const lastYear = new Date().getFullYear() - 1
const header = [
  {
    key: "name",
    label: "Nom de la cantine",
  },
  {
    key: "siret",
    label: "SIRET / SIREN",
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
    const name = canteensTableService.getNameInfos(canteen)
    const siret = canteensTableService.getSiretOrSirenInfos(canteen)
    const city = canteensTableService.getCityInfos(canteen)
    const productionType = canteensTableService.getProductionTypeInfos(canteen)
    const diagnostic = canteensTableService.getDiagnosticInfos(canteen, props.campaign)
    const actions = getDropdownLinks(canteen)

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

  if (canteen.productionType === "groupe") {
    links.push({
      to: { name: "GestionnaireCantineGroupeSatellites", params: { canteenUrlComponent: canteenUrlComponent } },
      label: "Gérer les restaurants satellites",
    })
  }
  return links
}
</script>
<template>
  <LayoutBigTable>
    <DsfrDataTable
      title="Vos cantines"
      no-caption
      :headers-row="header"
      :rows="rows"
      :pagination="true"
      :pagination-options="[50, 100, 200]"
      :rows-per-page="50"
      pagination-wrapper-class="fr-mt-4w"
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
            <router-link :to="{ name: 'GestionnaireCantineGroupeSatellites', params: { canteenUrlComponent: cell.url } }">
              {{ cell.satellitesCountSentence }}
            </router-link>
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
  </LayoutBigTable>
</template>
