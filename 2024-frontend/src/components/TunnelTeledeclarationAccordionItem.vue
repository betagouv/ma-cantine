<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import tunnelTeledeclarationService from '@/services/tunnelTeledeclaration'
import canteensTableService from '@/services/canteensTable.js'
import { formatSiretOrSiren } from '@/utils'
import CanteenDisplayInformations from '@/components/CanteenDisplayInformations.vue'
import TunnelTeledeclarationIconCheck from '@/components/TunnelTeledeclarationIconCheck.vue'

const props = defineProps(["accordion", "id"])

/* Router */
const router = useRouter()

/* Stores */
const canteenStore = useStoreCanteen()
const teledeclarationStore = useStoreTeledeclaration()
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnostic, diagnosticErrors, groupeCanteensMealCount } = storeToRefs(teledeclarationStore)

/* Errors */
const errors = computed(() => teledeclarationStore.getErrorsGroup(props.accordion.fieldsGroupName))
const hasErrors = computed(() => errors.value && errors.value?.length > 0)
const errorBadge = computed(() => {
  if (!hasErrors.value) return ""
  const count = errors.value.length
  const sentence = count > 1 ? 'erreurs détectées' : 'erreur détectée'
  return `${count} ${sentence}`
})

/* Data */
const header = [
  { key: "name", label: "Champ" },
  { key: "value", label: "Valeur", headerAttrs: { class: "fr-col-2" } },
]
const isGroupeMealCountField = (field) => props.accordion.fieldsGroupName === "couvertsGroupe" && field === "nombreRepasAn"

const getPrettyDiagnosticValue = (field) => {
  const fieldData = tunnelTeledeclarationService.getField(field)
  const hasOptions = fieldData?.options?.length > 0
  const diagValue = diagnostic.value[field]
  const prettyValue = hasOptions ? fieldData.options.find(option => option.value === diagValue)?.valueDisplay : diagValue
  return prettyValue ?? "Non renseigné"
}

const getRowName = (field) => {
  if (props.accordion.isCanteenFields) return { label: field }
  const { labelRecap, hint } = tunnelTeledeclarationService.getField(field)
  return { label: labelRecap, hint }
}

const getRowValue = (field) => {
  if (props.accordion.isCanteenFields) return canteenInformations.value[field]
  return getPrettyDiagnosticValue(field)
}

const getFieldRow = (field) => {
  // For a group : the field is replaced by the sum (the errors are still those of nombreRepasAn)
  const displayedField = isGroupeMealCountField(field) ? "satellitesNombreRepasAnSum" : field
  return {
    name: {
      ...getRowName(displayedField),
      error: teledeclarationStore.getErrorMessage(field) || "",
    },
    value: getRowValue(displayedField) ?? "Non renseigné",
  }
}

const getGroupeCanteenRow = (groupeCanteen) => {
  const siretSiren = formatSiretOrSiren(canteensTableService.getSiretOrSirenInfos(groupeCanteen))
  return {
    name: {
      label: groupeCanteen.name,
      hint: `${siretSiren}, ID : ${groupeCanteen.id}`,
      error: tunnelTeledeclarationService.getGroupeCanteenMealCountError(groupeCanteen, diagnosticErrors.value) || "",
    },
    value: groupeCanteen.nombreRepasAn ?? "Non renseigné",
  }
}

const rows = computed(() => {
  const fields = tunnelTeledeclarationService.getFieldsListFromGroup(props.accordion.fieldsGroupName)
  const fieldsRows = fields.filter(field => field !== "satellitesNombreRepasAnList").map(getFieldRow)
  const groupeCanteensRows = fields.includes("satellitesNombreRepasAnList") ? groupeCanteensMealCount.value.map(getGroupeCanteenRow) : []
  return fieldsRows.concat(groupeCanteensRows)
})

const goToStep = (page) => router.push(page)
</script>

<template>
  <DsfrAccordion :id="id" :title="accordion.title">
    <template #title>
      <TunnelTeledeclarationIconCheck type="group" :name="accordion.fieldsGroupName" class="fr-mr-1w" />
      {{ accordion.title }}
      <DsfrBadge v-if="hasErrors" :label="errorBadge" type="error" class="fr-ml-2w" />
    </template>
    <CanteenDisplayInformations
      v-if="accordion.isCanteenFields"
      :canteenInformation="canteenInformations"
      :canteenIsGroupe="canteenInformations.isGroupe"
    />
    <DsfrDataTable
      v-else
      title="Données enregistrées"
      no-caption
      :headersRow="header"
      :rows="rows"
      :no-scroll="true"
      class="fr-mt-0 fr-mb-0 tunnel-teledeclaration-accordion-item__table"
      size="sm"
    >
      <template #cell="{ colKey, cell }">
        <template v-if="colKey === 'name'">
          <p :class="{ 'fr-mb-0': cell.hint }">{{ cell.label }}</p>
          <p v-if="cell.hint" class="fr-text--xs fr-text-mention--grey">{{ cell.hint }}</p>
          <p v-if="cell.error" class="fr-message fr-message--error">{{ cell.error }}</p>
        </template>
        <p v-else>{{ cell }}</p>
      </template>
    </DsfrDataTable>
    <div class="ma-cantine--flex-end fr-mt-2w">
      <DsfrButton @click="goToStep(accordion.to)" secondary label="Modifier ces données" icon="ri-pencil-line" size="sm" />
    </div>
  </DsfrAccordion>
</template>

<style lang="scss">
.tunnel-teledeclaration-accordion-item__table {
  .fr-table__wrapper,
  table {
    width: 100% !important;
  }
}
</style>
