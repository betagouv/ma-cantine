<script setup>
import { computedAsync } from "@vueuse/core"
import canteenService from "@/services/canteens.js"
import badgeService from "@/services/badges.js"
import urlService from "@/services/urls.js"
import cantines from "@/data/cantines.json"

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
    label: "Commune et code postal",
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

const rows = computedAsync(async () => {
  const lastYear = new Date().getFullYear() - 1
  const canteens = await canteenService.fetchCanteensActions(lastYear)
  const rows = []
  canteens.forEach((canteen) => {
    const name = getNameInfos(canteen)
    const siret = getSiretOrSirenInfos(canteen)
    const city = getCityInfos(canteen)
    const productionType = getProductionTypeInfos(canteen)
    const status = getStatusInfos(canteen)

    rows.push({
      name,
      siret,
      city,
      productionType,
      status,
      actions: "",
    })
  })
  return rows
}, [])

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
  const badge = badgeService.getFromAction(action)
  return {
    label: badge.body,
    type: badge.mode,
  }
}
</script>
<template>
  <DsfrDataTable class="gestionnaire-canteens-table" title="Vos cantines" no-caption :headers-row="header" :rows="rows">
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
      <template v-else>
        <p class="fr-text--xs">{{ cell }}</p>
      </template>
    </template>
  </DsfrDataTable>
</template>

<style lang="scss">
.gestionnaire-canteens-table {
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
