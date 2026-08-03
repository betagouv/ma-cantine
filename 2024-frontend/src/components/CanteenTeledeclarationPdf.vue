<script setup>
import { computed } from "vue"
const props = defineProps(["diagnostic", "canteenId"])

const isTeledeclared = computed(() => props.diagnostic.isTeledeclared)
const isInvalid = computed(() => !props.diagnostic.declarationDonnees)
const hasGeneratedFromGroupe = computed(() => props.diagnostic.generatedFromGroupeDiagnosticId !== null)
const groupeOverrideTd = computed(() => props.diagnostic.generatedFromGroupeDiagnosticMode === "ALL")

const badge = computed(() => {
  switch (true) {
    case isTeledeclared.value && isInvalid.value:
      return {
        type: "warning",
        label: "Télédéclaré - erreur(s) détectée(s)"
      }
    case isTeledeclared.value && !isInvalid.value:
      return {
        type: "success",
        label: "Télédéclaré"
      }
    default:
      return {
        type: "neutral",
        label: "Non télédéclaré"
      }
  }
})

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
  <li class="canteen-teledeclaration-pdf fr-pb-2w fr-my-1w">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top">
      <div class="fr-col-12 fr-col-md-3">
        <p class="fr-mb-0 fr-text--bold">Ma télédéclaration {{ diagnostic.year }}</p>
      </div>
      <div class="canteen-teledeclaration-pdf__right fr-col-12 fr-col-md-9">
        <DsfrBadge :label="badge.label" :type="badge.type" />
        <div class="ma-cantine--flex-start ma-cantine--flex-gap-1">
          <a v-if="canteenLink" :href="canteenLink" target="_self" download class="fr-text-title--blue-france">
            <span class="fr-icon-file-download-fill ma-cantine--icon-xs" aria-hidden="true"></span>
            Télécharger mon justificatif
          </a>
          <a v-if="generatedFromGroupeLink" :href="generatedFromGroupeLink" target="_self" download class="fr-text-title--blue-france">
            <span class="fr-icon-file-download-fill ma-cantine--icon-xs" aria-hidden="true"></span>
            Télécharger le justificatif de mon groupe
          </a>
        </div>
      </div>
    </div>
  </li>
</template>

<style lang="scss">
.canteen-teledeclaration-pdf {
  &__right {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    row-gap: 0.5rem;
  }
}
</style>
