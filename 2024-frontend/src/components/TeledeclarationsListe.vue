<script setup>
import { computed } from "vue"
const props = defineProps(["diagnostics", "groupeDiagnostics", "canteenId"])

const firstYear = 2021
const lastYear = new Date().getFullYear() - 1

const getDiagForYear = (year, list) => {
  if (!list) return []
  return list.filter(diagnostic => diagnostic.year === year)
}

const teledeclarations = computed(() => {
  const teledeclarations = []
  for (let year = lastYear; year >= firstYear; year--) {
    const diag = getDiagForYear(year, props.diagnostics)
    const isTeledeclared = diag.length > 0 ? diag[0].isTeledeclared : false
    const url = isTeledeclared ? `/api/v1/canteens/${props.canteenId}/diagnostics/${diag[0].id}/teledeclaration/pdf` : null
    teledeclarations.push({
      year,
      isTeledeclared,
      url
    })
  }
  return teledeclarations
})
</script>

<template>
  <ul class="ma-cantine--unstyled-list">
    <li v-for="teledeclaration in teledeclarations" :key="teledeclaration.year" class="fr-grid-row fr-grid-row--gutters fr-grid-row--middle">
      <div class="fr-col-12 fr-col-md-3">
        <p class="fr-mb-0">Ma télédéclaration {{ teledeclaration.year }}</p>
      </div>
      <div class="fr-col-12 fr-col-md-9">
        <a v-if="teledeclaration.isTeledeclared" :href="teledeclaration.url" target="_self" download class="fr-text-title--blue-france">
          <span class="fr-icon-file-download-fill ma-cantine--icon-xs" aria-hidden="true"></span>
          Télécharger mon justificatif
        </a>
        <DsfrBadge v-if="!teledeclaration.isTeledeclared" label="Non télédéclaré" type="neutral" />
      </div>
    </li>
  </ul>
</template>
