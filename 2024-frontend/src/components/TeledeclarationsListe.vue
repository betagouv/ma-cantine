<script setup>
import { computed } from "vue"
const props = defineProps(["diagnostics", "groupeDiagnostics", "canteenId"])

const firstYear = 2021
const lastYear = new Date().getFullYear() - 1

const getDiagForYear = (year, list) => {
  if (!list) return []
  return list.filter(diagnostic => diagnostic.year === year)
}

const getDataCanteen = (year) => {
  const canteenDiag = getDiagForYear(year, props.diagnostics)
  if (canteenDiag.length === 0) return {isTeledeclared: false, url: null}
  const isTeledeclared = canteenDiag.length > 0 ? canteenDiag[0].isTeledeclared : false
  const url = isTeledeclared ? `/api/v1/canteens/${props.canteenId}/diagnostics/${canteenDiag[0].id}/teledeclaration/pdf` : null
  return {isTeledeclared, url}
}

const getDataGroupe = (year) => {
  const groupeDiag = getDiagForYear(year, props.groupeDiagnostics)
  const isTeledeclaredByGroupe = groupeDiag.length > 0 ? groupeDiag[0].isTeledeclared : false
  const groupeDiagMode = groupeDiag.length > 0 ? groupeDiag[0].centralKitchenDiagnosticMode : null
  return { isTeledeclaredByGroupe, groupeDiagMode }
}

const getBadge = (isTeledeclared, isTeledeclaredByGroupe, groupeDiagMode) => {
  switch (true) {
    case !isTeledeclared && !isTeledeclaredByGroupe:
      return {
        type: "neutral",
        label: "Non télédéclaré",
      }
    case groupeDiagMode === "ALL" && isTeledeclaredByGroupe:
      return {
        type: "success",
        label: "Télédéclaré par votre groupe",
      }
    case groupeDiagMode === "APPRO" && isTeledeclaredByGroupe:
      return {
        type: "success",
        label: "Approvisionnement télédéclaré par votre groupe",
      }
  }
}

const teledeclarations = computed(() => {
  const teledeclarations = []
  for (let year = lastYear; year >= firstYear; year--) {
    const { isTeledeclared, url } = getDataCanteen(year)
    const { isTeledeclaredByGroupe, groupeDiagMode } = getDataGroupe(year)
    const badge = getBadge(isTeledeclared, isTeledeclaredByGroupe, groupeDiagMode)
    teledeclarations.push({
      year,
      url: isTeledeclaredByGroupe && groupeDiagMode === "ALL" ? null : url,
      badge,
    })
  }
  return teledeclarations
})
</script>

<template>
  <ul class="teledeclarations-liste ma-cantine--unstyled-list">
    <li v-for="teledeclaration in teledeclarations" :key="teledeclaration.year" class="teledeclarations-liste__item fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-pb-1w fr-my-1w">
      <div class="fr-col-12 fr-col-md-3">
        <p class="fr-mb-0">Ma télédéclaration {{ teledeclaration.year }}</p>
      </div>
      <div class="teledeclarations-liste__justificatif fr-col-12 fr-col-md-9">
        <a v-if="teledeclaration.url" :href="teledeclaration.url" target="_self" download class="fr-text-title--blue-france">
          <span class="fr-icon-file-download-fill ma-cantine--icon-xs" aria-hidden="true"></span>
          Télécharger mon justificatif
        </a>
        <DsfrBadge v-if="teledeclaration.badge" :label="teledeclaration.badge.label" :type="teledeclaration.badge.type" />
      </div>
    </li>
  </ul>
</template>

<style lang="scss">
.teledeclarations-liste {
  &__item {
    border-bottom: solid 1px var(--border-disabled-grey);
  }

  &__justificatif {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    row-gap: 1rem;
  }
}
</style>
