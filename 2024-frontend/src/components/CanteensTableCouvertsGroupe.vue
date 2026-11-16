<script setup>
import { computed, ref } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { formatSiretOrSiren } from "@/utils"
import canteensTableService from "@/services/canteensTable.js"

/* Settings */
const minPagination = 50
const teledeclarationStore = useStoreTeledeclaration()
const { groupeCanteensMealCount } = storeToRefs(teledeclarationStore)
const showPagination = computed(() => groupeCanteensMealCount.value.length > minPagination)
const errors = ref({})

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
  },
  {
    key: "siretSiren",
    label: "SIRET / SIREN",
  },
  {
    key: "id",
    label: "ID",
  },
  {
    key: "status",
    label: "Statut",
  },
  {
    key: "mealCount",
    label: "Couverts / an",
  },
]

const tableRows = computed(() => {
  return groupeCanteensMealCount.value.map((canteen) => {
    const canteenSiretOrSiren = canteensTableService.getSiretOrSirenInfos(canteen)
    return {
      name: canteen.name,
      siretSiren: formatSiretOrSiren(canteenSiretOrSiren),
      id: canteen.id,
      status: "",
      mealCount: {
        id: canteen.id,
        name: canteen.name,
        value: canteen.nombreRepasAn,
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
    pagination-wrapper-class="ma-cantine--table-pagination fr-mt-4w"
  >
    <template #cell="{ colKey, cell }">
      <template v-if="colKey === 'name'">
        <span class="fr-text--bold">{{ cell }}</span>
      </template>
      <template v-else-if="colKey === 'mealCount'">
        <DsfrInputGroup
          :model-value="cell.value"
          :label="`Couverts / an de ${cell.name}`"
          :label-visible="false"
          :name="`mealCount-${cell.id}`"
          type="number"
          min="0"
          :error-message="errors[cell.id]"
          @change="(event) => updateMealCount(cell.id, event.target.value)"
        />
      </template>
      <template v-else>
        {{ cell }}
      </template>
    </template>
  </DsfrDataTable>
</template>
