<script setup>
import FilterByYears from "@/components/FilterByYears.vue"
import FilterByCharacteristics from "@/components/FilterByCharacteristics.vue"
import FilterBySectors from "@/components/FilterBySectors.vue"
import FilterByCities from "@/components/FilterByCities.vue"
import FilterByPAT from "@/components/FilterByPAT.vue"
import FilterByEPCI from "@/components/FilterByEPCI.vue"
</script>

<template>
  <div class="app-filters">
    <p class="app-filters__title fr-mb-0">Filtrer par :</p>
    <div class="fr-grid-row">
      <FilterByEPCI class="fr-mr-1v fr-mb-1v" />
      <FilterByPAT class="fr-mr-1v fr-mb-1v" />
      <FilterByCities class="fr-mr-1v fr-mb-1v" />
      <div class="fr-col-12 fr-hidden fr-unhidden-md"></div>
      <FilterBySectors class="fr-mr-1v fr-mb-1v" />
      <FilterByCharacteristics class="fr-mr-1v fr-mb-1v" />
      <FilterByYears class="fr-mr-1v fr-mb-1v" />
    </div>
  </div>
</template>

<style lang="scss">
.app-filters {
  display: flex;
  justify-content: flex-start;
  align-items: baseline;
  flex-direction: column;
  gap: 1rem;

  @media (min-width: 768px) {
    flex-direction: row;
  }

  &__title {
    flex-shrink: 0;
  }
}
</style>
