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

const getPrettyDiagnosticValue = (field) => {
  const fieldData = tunnelTeledeclarationService.getField(field)
  const hasOptions = fieldData?.options?.length > 0
  const diagValue = diagnostic.value[field]
  const prettyValue = hasOptions ? fieldData.options.find(option => option.value === diagValue)?.valueDisplay : diagValue
  return prettyValue ?? "Non renseigné"
}

const getRowName = (field, canteen) => {
  if (canteen) {
    const siretSiren = formatSiretOrSiren(canteensTableService.getSiretOrSirenInfos(canteen))
    return `${canteen.name} ${siretSiren} (ID : ${canteen.id})`
  }
  if (props.accordion.isCanteenFields) return field
  return tunnelTeledeclarationService.getField(field).labelRecap
}

const getRowValue = (field, canteen) => {
  if (canteen) return canteen.nombreRepasAn
  if (props.accordion.isCanteenFields) return canteenInformations.value[field]
  return getPrettyDiagnosticValue(field)
}

const getRowError = (field, canteen) => {
  if (canteen) return tunnelTeledeclarationService.getGroupeCanteenMealCountError(canteen, diagnosticErrors.value)
  return teledeclarationStore.getErrorMessage(field)
}

const rows = computed(() => {
  const fields = tunnelTeledeclarationService.getFieldsListFromGroup(props.accordion.fieldsGroupName)
  return fields.flatMap(field => {
    const canteens = field === "satellitesNombreRepasAnList" ? groupeCanteensMealCount.value : [null]
    return canteens.map(canteen => ({
      name: {
        label: getRowName(field, canteen),
        error: getRowError(field, canteen) || "",
      },
      value: getRowValue(field, canteen) ?? "Non renseigné",
    }))
  })
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
      class="fr-mt-0 fr-mb-0"
      size="sm"
    >
      <template #cell="{ colKey, cell }">
        <template v-if="colKey === 'name'">
          <p>{{ cell.label }}</p>
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
