<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import tunnelTeledeclarationService from "@/services/tunnelTeledeclaration"

const props = defineProps(["type", "name"])
const router = useRouter()
const canteenStore = useStoreCanteen()
const teledeclarationStore = useStoreTeledeclaration()
const getPageFromName = (pageName) => router.resolve({ name: pageName }).meta
const pageName = computed(() => {
  if (props.type === "group") return tunnelTeledeclarationService.getPageFromFieldsGroup(props.name)
  const isCouvertsGroupe = props.name === "GestionnaireTunnelApproCouverts" && canteenStore.canteenInformations?.isGroupe
  return isCouvertsGroupe ? "GestionnaireTunnelApproCouvertsGroupe" : props.name
})

const isVisited = computed(() => {
  const page = props.type === "volet" ? { volet: props.name } : getPageFromName(pageName.value)
  return teledeclarationStore.isPageVisited(page)
})

const isValid = computed(() => {
  if (!isVisited.value) return false
  if (props.type === "volet") return teledeclarationStore.isVoletFilled(props.name) && teledeclarationStore.isVoletClean(props.name)
  if (props.type === "group") return teledeclarationStore.getErrorsGroup(props.name).length === 0
  if (props.type === "page") return teledeclarationStore.getErrorsPage(pageName.value, canteenStore.canteenInformations?.isGroupe).length === 0
  return false
})

const iconClasses = computed(() => {
  const color = isValid.value ? "default--success" : "mention--grey"
  const shape = isValid.value ? "fill" : "line"
  return `fr-icon-checkbox-circle-${shape} fr-text-${color}`
})
</script>

<template>
  <span :class="iconClasses" class="ma-cantine--icon-xs"></span>
</template>
