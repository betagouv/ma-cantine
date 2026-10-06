<script setup>
import { computed } from "vue"
import DiagnosticPdf from "@/components/DiagnosticPdf.vue"

const props = defineProps(["diagnostic", "canteenId"])

const isTeledeclared = computed(() => props.diagnostic.isTeledeclared)
const isInvalid = computed(() => !props.diagnostic.declarationDonnees)

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
</script>

<template>
  <li class="canteen-diagnostics-list fr-py-2w fr-my-1w">
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top">
      <div class="fr-col-12 fr-col-md-3">
        <p class="fr-mb-0 fr-text--bold">Ma télédéclaration {{ diagnostic.year }}</p>
      </div>
      <div class="canteen-diagnostics-list__right fr-col-12 fr-col-md-9">
        <DsfrBadge :label="badge.label" :type="badge.type" />
        <DiagnosticPdf :diagnostic="diagnostic" :canteenId="canteenId" />
      </div>
    </div>
  </li>
</template>

<style lang="scss">
.canteen-diagnostics-list {
  &__right {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    row-gap: 0.5rem;
  }
}
</style>
