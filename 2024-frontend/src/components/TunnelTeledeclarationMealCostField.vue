<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import tunnelTeledeclarationService from "@/services/tunnelTeledeclaration.js"
import TunnelTeledeclarationCalloutField from "@/components/TunnelTeledeclarationCalloutField.vue"

const coutRepasFieldName = tunnelTeledeclarationService.getFieldsListFromGroup("coutRepas")[0]
const { diagnostic } = storeToRefs(useStoreTeledeclaration())
const coutRepas = computed(() => diagnostic.value[coutRepasFieldName] || '-')
</script>

<template>
  <TunnelTeledeclarationCalloutField text="Le coût repas moyen représente :" :value="coutRepas" />
</template>
