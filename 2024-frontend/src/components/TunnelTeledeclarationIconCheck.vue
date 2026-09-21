<script setup>
import { computed } from "vue"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"

const props = defineProps(["fieldsGroupName", "fieldsPageName"])
const teledeclarationStore = useStoreTeledeclaration()
const errors = computed(() => {
  if (props.fieldsGroupName) return teledeclarationStore.getErrorsGroup(props.fieldsGroupName)
  if (props.fieldsPageName) return teledeclarationStore.getErrorsPage(props.fieldsPageName)
  return []
})
const hasErrors = computed(() => errors.value && errors.value?.length > 0)

const iconClasses = computed(() => {
  const color = hasErrors.value ? "mention--grey" : "default--success"
  const shape = hasErrors.value ? "line" : "fill"
  return `fr-icon-checkbox-circle-${shape} fr-text-${color}`
})
</script>

<template>
  <span :class="iconClasses" class="ma-cantine--icon-xs"></span>
</template>
