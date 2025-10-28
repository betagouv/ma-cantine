<script setup>
import { computedAsync } from "@vueuse/core"
import canteenService from "@/services/canteens.js"
import badgeService from "@/services/badges.js"
import urlService from "@/services/urls.js"
import cantines from "@/data/cantines.json"

/* Table */
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
  const canteens = await canteenService.fetchCanteensActions()
  const rows = []
  canteens.forEach((canteen) => {
    const badge = badgeService.getFromAction(canteen.action)
    rows.push({
      name: {
        name: canteen.name,
        url: urlService.getCanteenUrl(canteen),
      },
      siret: canteen.siret || canteen.sirenUniteLegale,
      city: {
        name: canteen.city,
        postalCode: canteen.postalCode,
        isEmpty: !canteen.city && !canteen.postalCode,
      },
      productionType: getProductionTypeLabel(canteen.productionType),
      status: {
        label: badge.body,
        type: badge.mode,
      },
      actions: "",
    })
  })
  return rows
}, [])

const getProductionTypeLabel = (slug) => {
  const index = cantines.productionType.findIndex((type) => type.value === slug)
  return cantines.productionType[index].label
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
      <template v-else-if="colKey === 'city'">
        <p class="fr-text--xs">
          <span v-if="cell.isEmpty">Non renseigné</span>
          <span v-if="cell.name">
            {{ cell.name }}
            <br />
          </span>
          <span v-if="cell.postalCode">
            {{ cell.postalCode }}
          </span>
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
  &__table {
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
}
</style>
