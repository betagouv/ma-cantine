<script setup>
import { useTemplateRef } from "vue"
import FilterByYears from "@/components/FilterByYears.vue"
import FilterByCharacteristics from "@/components/FilterByCharacteristics.vue"
import FilterBySectors from "@/components/FilterBySectors.vue"
import FilterByCities from "@/components/FilterByCities.vue"
import FilterByPATs from "@/components/FilterByPATs.vue"
import FilterByEPCIs from "@/components/FilterByEPCIs.vue"
import FilterByDepartments from "@/components/FilterByDepartments.vue"
import FilterByRegions from "@/components/FilterByRegions.vue"

const anchor = useTemplateRef("anchor")
defineExpose({ anchor })
</script>

<template>
  <section class="observatory-filters fr-pt-5w" ref="anchor">
    <h2 class="fr-h5">Retrouver les chiffres clés sur votre territoire</h2>
    <div class="observatory-filters__container">
      <p class="observatory-filters__title fr-mb-0">Filtrer par :</p>
      <div class="observatory-filters__list fr-grid-row">
        <FilterByYears class="fr-mr-1v fr-mb-1v" />
        <FilterByRegions class="fr-mr-1v fr-mb-1v" />
        <FilterByDepartments class="fr-mr-1v fr-mb-1v" />
        <FilterByEPCIs class="fr-mr-1v fr-mb-1v" />
        <FilterByPATs class="fr-mr-1v fr-mb-1v" />
        <FilterByCities class="fr-mr-1v fr-mb-1v" />
        <FilterBySectors class="fr-mr-1v fr-mb-1v" />
        <FilterByCharacteristics class="fr-mr-1v fr-mb-1v" />
      </div>
    </div>
  </section>
</template>

<style lang="scss">
.observatory-filters {
  &__container {
    display: flex;
    justify-content: flex-start;
    align-items: baseline;
    flex-direction: column;
    gap: 1rem;

    @media (min-width: 768px) {
      flex-direction: row;
    }
  }

  &__list {
    flex-direction: column;

    @media (min-width: 768px) {
      flex-direction: row;
    }
  }

  &__title {
    flex-shrink: 0;
  }
}
</style>
