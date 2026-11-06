<script setup>
import { computed } from "vue"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"

const props = defineProps(["fieldsGroupName", "fieldsPageName", "slug", "volet"])
const teledeclarationStore = useStoreTeledeclaration()
const errors = computed(() => {
  if (props.fieldsGroupName) return teledeclarationStore.getErrorsGroup(props.fieldsGroupName)
  if (props.fieldsPageName) return teledeclarationStore.getErrorsPage(props.fieldsPageName)
  return []
})
const hasErrors = computed(() => errors.value && errors.value?.length > 0)
const isVisited = computed(() => {
  if (props.volet) return teledeclarationStore.isVoletVisited(props.volet)
  return !props.slug || teledeclarationStore.isPageVisited(props.slug)
})
const isClean = computed(() => !props.volet || teledeclarationStore.isVoletClean(props.volet))
const isValid = computed(() => isVisited.value && isClean.value && !hasErrors.value)

const iconClasses = computed(() => {
  const color = isValid.value ? "default--success" : "mention--grey"
  const shape = isValid.value ? "fill" : "line"
  return `fr-icon-checkbox-circle-${shape} fr-text-${color}`
})
</script>

<template>
  <span :class="iconClasses" class="ma-cantine--icon-xs"></span>
</template>
