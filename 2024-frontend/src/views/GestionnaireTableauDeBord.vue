<script setup>
import { computed } from "vue"
import { computedAsync } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import badgeService from "@/services/badges.js"
import urlService from "@/services/urls.js"
import cantines from "@/data/cantines.json"
import GestionnaireGuides from "@/components/GestionnaireGuides.vue"
import GestionnaireCanteensCreate from "@/components/GestionnaireCanteensCreate.vue"

const store = useRootStore()

/* Title */
const canteenSentence = computed(() => {
  const count = store.canteenPreviews.length
  if (count === 0) return "vous n'avez pas encore de cantine"
  else if (count === 1) return "1 cantine"
  return `${count} cantines`
})

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
  <section>
    <h1>Bienvenue dans votre espace, {{ store.loggedUser.firstName }}</h1>
    <p class="fr-text--lead">{{ canteenSentence }}</p>
  </section>
  <section class="ma-cantine--stick-to-footer">
    <GestionnaireCanteensCreate v-if="store.canteenPreviews.length === 0" />
    <DsfrDataTable
      v-else
      class="gestionnaire-tableau-de-bord__table"
      title="Vos cantines"
      no-caption
      :headers-row="header"
      :rows="rows"
    >
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
    <GestionnaireGuides />
  </section>
</template>

<style lang="scss">
.gestionnaire-tableau-de-bord {
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
