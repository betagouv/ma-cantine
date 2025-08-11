<script setup>
import { ref, computed, onMounted, onUnmounted, useTemplateRef } from "vue"
import { useStoreFilters } from "@/stores/filters"

const storeFilters = useStoreFilters()
const filtersList = computed(() => storeFilters.getSelection())

/* Change styles depending on scroll */
const filtersSelectedHtml = useTemplateRef("filters-selected-html")
const displaySmallFilters = ref(false)
const scroll = () => {
  const bounding = filtersSelectedHtml.value.getBoundingClientRect()
  const isStickToTop = bounding.top <= 0
  if (isStickToTop && !displaySmallFilters.value) displaySmallFilters.value = true
  if (!isStickToTop && displaySmallFilters.value) displaySmallFilters.value = false
}

/* Scroll watchers */
onMounted(() => {
  window.addEventListener("scroll", scroll)
})
onUnmounted(() => {
  window.removeEventListener("scroll", scroll)
})
</script>

<template>
  <div
    ref="filters-selected-html"
    class="observatory-filters-selected ma-cantine--sticky__top fr-py-2w fr-background-alt--blue-france"
    :class="{ small: displaySmallFilters }"
  >
    <p class="observatory-filters-selected__title fr-mb-0">Chiffres clés pour la recherche :</p>
    <div class="observatory-filters-selected__scrollable">
      <ul class="observatory-filters-selected__list ma-cantine--unstyled-list fr-my-0">
        <li v-for="(filter, index) in filtersList" :key="index" class="observatory-filters-selected__item">
          <DsfrTag
            @click="storeFilters.remove(filter.name, filter.value)"
            :label="filter.label"
            class="fr-tag--dismiss"
            tagName="button"
          />
        </li>
      </ul>
    </div>
    <DsfrButton
      class="observatory-filters-selected__button"
      tertiary
      label="Modifier les filtres"
      icon="fr-icon-filter-fill"
      @click="$emit('scrollToFilters')"
    />
  </div>
</template>

<style lang="scss">
.observatory-filters-selected {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  &__title {
    flex-shrink: 0;
  }

  &__scrollable {
    flex-grow: 1;
    flex-shrink: 1;
  }

  &__list {
    justify-content: flex-start;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  &__item {
    flex-shrink: 0;
  }

  &__button {
    display: none !important;
    flex-shrink: 0;
  }

  &.small {
    align-items: center;

    .observatory-filters-selected {
      &__list {
        flex-shrink: 0;
      }

      &__scrollable,
      &__title {
        display: none;
      }

      &__button {
        display: inline-flex !important;
        align-self: flex-end;
      }
    }
  }

  @media (min-width: 768px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: baseline;

    &.small {
      .observatory-filters-selected {
        &__title {
          display: initial;
        }

        &__scrollable {
          max-height: 2rem;
          overflow-x: scroll;
          display: flex;
        }
      }
    }
  }
}
</style>
