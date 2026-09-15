<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useStoreCanteen } from '@/stores/canteen'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import teledeclaration from '@/data/teledeclaration.json'
import CanteenDisplayInformations from '@/components/CanteenDisplayInformations.vue'

const props = defineProps(["accordion", "id"])

/* Router */
const router = useRouter()

/* Stores */
const canteenStore = useStoreCanteen()
const teledeclarationStore = useStoreTeledeclaration()
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnostic } = storeToRefs(teledeclarationStore)

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
  { key: "value", label: "Valeur" },
]

const getPrettyDiagnosticValue = (field) => {
  const hasOptions = teledeclaration.fields[field]?.options?.length > 0
  const diagValue = diagnostic.value[field]
  const prettyValue = hasOptions ? teledeclaration.fields[field].options.find(option => option.value === diagValue).labelShort : diagValue
  return prettyValue !== null ? prettyValue : "Non renseigné"
}

const rows = computed(() => {
  const fields = teledeclaration.groups[props.accordion.fieldsGroupName]
  return fields.map(field => {
    const isCanteen = props.accordion.isCanteenFields
    const name = isCanteen ? field : teledeclaration.fields[field].label
    const value = isCanteen ? canteenInformations.value[field] : getPrettyDiagnosticValue(field)
    return {
      name,
      value,
    }
  })
})

const goToStep = (page) => router.push(page)
</script>

<template>
  <DsfrAccordion :id="id" :title="accordion.title">
    <template #title>
      {{ accordion.title }}
      <DsfrBadge v-if="hasErrors" :label="errorBadge" type="error" class="fr-ml-2w" />
    </template>
    <DsfrButton label="Modifier ces données" @click="goToStep(accordion.to)" icon="ri-pencil-line" secondary size="sm" class="fr-mb-2w" />
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
    />
  </DsfrAccordion>
</template>
