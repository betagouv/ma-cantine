<script setup>
import { computed } from "vue"
const props = defineProps(["diagnostic", "canteenId"])

const isTeledeclared = computed(() => props.diagnostic.isTeledeclared)
const hasGeneratedFromGroupe = computed(() => props.diagnostic.generatedFromGroupeDiagnosticId !== null)
const groupeOverrideTd = computed(() => props.diagnostic.generatedFromGroupeDiagnosticMode === "ALL")

const canteenLink = computed(() => {
  if (!isTeledeclared.value) return null
  if (hasGeneratedFromGroupe.value && groupeOverrideTd.value) return null
  return`/api/v1/canteens/${props.canteenId}/diagnostics/${props.diagnostic.canteenDiagnosticId}/teledeclaration/pdf`
})

const generatedFromGroupeLink = computed(() => {
  if (!props.diagnostic.generatedFromGroupeDiagnosticId) return null
  return `/api/v1/canteens/${props.canteenId}/diagnostics/${props.diagnostic.generatedFromGroupeDiagnosticId}/teledeclaration/pdf`
})
</script>

<template>
  <div>
    <p v-if="canteenLink" class="fr-mb-1w">
      <a :href="canteenLink" target="_self" download class="fr-text-title--blue-france">
        <span class="fr-icon-file-download-fill ma-cantine--icon-xs" aria-hidden="true"></span>
        Télécharger mon justificatif
      </a>
    </p>
    <p v-if="generatedFromGroupeLink" class="fr-mb-1w">
      <a :href="generatedFromGroupeLink" target="_self" download class="fr-text-title--blue-france">
        <span class="fr-icon-file-download-fill ma-cantine--icon-xs" aria-hidden="true"></span>
        Télécharger le justificatif de mon groupe
      </a>
    </p>
  </div>
</template>
