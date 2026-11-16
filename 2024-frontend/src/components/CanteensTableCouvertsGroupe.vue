<script setup>
import { computed, ref } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { formatSiretOrSiren } from "@/utils"
import canteensTableService from "@/services/canteensTable.js"
import tunnelTeledeclarationService from "@/services/tunnelTeledeclaration"

/* Settings */
const minPagination = 50
const teledeclarationStore = useStoreTeledeclaration()
const { groupeCanteensMealCount } = storeToRefs(teledeclarationStore)
const showPagination = computed(() => groupeCanteensMealCount.value.length > minPagination)
const errors = ref({})
const route = useRoute()
const displayedErrors = computed(() => teledeclarationStore.getDisplayedErrors(route.meta))

/* Total */
const canteenSentence = computed(() => {
  const count = groupeCanteensMealCount.value.length
  if (count <= 1) return `${count} cantine`
  return `${count} cantines`
})

/* Table */
const tableHeaders = [
  {
    key: "name",
    label: "Nom de la cantine",
    headerAttrs: { style: { width: "30%" } },
  },
  {
    key: "siretSiren",
    label: "SIRET / SIREN",
    headerAttrs: { style: { width: "15%" } },
  },
  {
    key: "id",
    label: "ID",
    headerAttrs: { style: { width: "10%" } },
  },
  {
    key: "status",
    label: "Statut",
    headerAttrs: { style: { width: "15%" } },
  },
  {
    key: "mealCount",
    label: "Couverts / an",
    headerAttrs: { style: { width: "30%" } },
  },
]

const tableRows = computed(() => {
  return groupeCanteensMealCount.value.map((canteen) => {
    const canteenSiretOrSiren = canteensTableService.getSiretOrSirenInfos(canteen)
    const error = errors.value[canteen.id] || tunnelTeledeclarationService.getGroupeCanteenMealCountError(canteen, displayedErrors.value)
    return {
      name: canteen.name,
      siretSiren: formatSiretOrSiren(canteenSiretOrSiren),
      id: canteen.id,
      status: error ? "Erreur" : "",
      mealCount: {
        id: canteen.id,
        name: canteen.name,
        value: canteen.nombreRepasAn,
        error,
      },
    }
  })
})

/* Actions */
const updateMealCount = async (id, value) => {
  const nombreRepasAn = value === "" ? null : Number(value)
  const response = await teledeclarationStore.updateGroupCanteenMealCount(id, nombreRepasAn)
  errors.value[id] = response?.status === "error" ? response.message : null
}
</script>

<template>
  <p class="fr-mb-0 fr-text--lead">{{ canteenSentence }}</p>
  <DsfrDataTable
    title="Répartition des couverts annuels entre mes cantines"
    no-caption
    :headers-row="tableHeaders"
    :rows="tableRows"
    :sortable-rows="['status']"
    :pagination="showPagination"
    :pagination-options="[minPagination, 100, 200]"
    :rows-per-page="minPagination"
    class="canteens-table-couverts-groupe"
    pagination-wrapper-class="ma-cantine--table-pagination fr-mt-4w"
  >
    <template #cell="{ colKey, cell }">
      <template v-if="colKey === 'name'">
        <span class="fr-text--bold">{{ cell }}</span>
      </template>
      <template v-else-if="colKey === 'status'">
        <DsfrBadge v-if="cell" :label="cell" type="error" small />
      </template>
      <template v-else-if="colKey === 'mealCount'">
        <DsfrInputGroup
          :model-value="cell.value"
          :label="`Couverts / an de ${cell.name}`"
          :label-visible="false"
          :name="`mealCount-${cell.id}`"
          type="number"
          min="0"
          :error-message="cell.error"
          @change="(event) => updateMealCount(cell.id, event.target.value)"
        />
      </template>
      <template v-else>
        {{ cell }}
      </template>
    </template>
  </DsfrDataTable>
</template>

<style lang="scss">
.canteens-table-couverts-groupe {
  .fr-error-text {
    white-space: pre-wrap;
  }
}
</style>
