<script setup>
import { computed } from "vue"
import { useStoreFilters } from "@/stores/filters"

const storeFilters = useStoreFilters()
const filtersList = computed(() => storeFilters.getFilled())
</script>

<template>
  <div class="observatory-results-filters ma-cantine--sticky__top fr-pt-4w fr-background-alt--blue-france">
    <p class="observatory-results-filters__title fr-mb-0">Chiffres clés pour la recherche :</p>
    <ul class="observatory-results-filters__list ma-cantine--unstyled-list">
      <li v-for="(filter, index) in filtersList" :key="index" class="r-mr-1w">
        <DsfrTag
          @click="storeFilters.remove(filter.name, filter.value)"
          :label="filter.label"
          class="fr-tag--dismiss"
          tagName="button"
        />
      </li>
    </ul>
    <DsfrButton
      class="observatory-results-filters__button"
      tertiary
      label="Modifier les filtres"
      icon="fr-icon-filter-fill"
      @click="$emit('scrollToFilters')"
    />
  </div>
</template>

<style lang="scss">
.observatory-results-filters {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  @media (min-width: 768px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: baseline;
  }

  &__title {
    flex-shrink: 0;
  }

  &__list {
    justify-content: flex-start;
    flex-grow: 1;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    flex-shrink: 1;
  }

  &__button {
    flex-shrink: 0;
  }
}
</style>
