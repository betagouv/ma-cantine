<script setup>
import { ref, watchEffect, useTemplateRef } from "vue"
import { useStoreFilters } from "@/stores/filters"
import statisticsService from "@/services/statistics"
import ObservatoryHero from "@/components/ObservatoryHero.vue"
import ObservatoryFilters from "@/components/ObservatoryFilters.vue"
import ObservatoryFiltersSelected from "@/components/ObservatoryFiltersSelected.vue"
import ObservatoryNumbers from "@/components/ObservatoryNumbers.vue"
import ObservatoryError from "@/components/ObservatoryError.vue"
import ObservatoryPurchases from "@/components/ObservatoryPurchases.vue"
import ObservatoryWarnings from "@/components/ObservatoryWarnings.vue"
import ObservatoryCanteens from "@/components/ObservatoryCanteens.vue"

/* Back to filters */
const observatoryFilters = useTemplateRef("observatory-filters")
const scrollToFilters = () => {
  observatoryFilters.value.anchor.scrollIntoView({ behavior: "smooth" })
}

/* Filters */
const storeFilters = useStoreFilters()
const filtersParams = storeFilters.getAllParams()

/* Stats */
const stats = ref()
const statsError = ref()

const setStatsError = () => {
  const hasNoFilter = storeFilters.getSelection().length === 0
  const hasNoYear = !storeFilters.getParam("year")
  statsError.value = "other"
  if (hasNoFilter) statsError.value = "noFilter"
  else if (hasNoYear) statsError.value = "noYear"
}

const resetStatsValue = () => {
  stats.value = null
  statsError.value = null
}

/* Watch filters */
watchEffect(async () => {
  resetStatsValue()
  const newStats = await statisticsService.getStatistics(filtersParams)
  if (!newStats) setStatsError()
  else stats.value = newStats
})
</script>

<template>
  <ObservatoryHero />
  <ObservatoryFilters ref="observatory-filters" />
  <section class="observatoire__results ma-cantine--sticky__container fr-mt-4w fr-pt-2w fr-pb-4w">
    <ObservatoryFiltersSelected @scrollToFilters="scrollToFilters()" class="ma-cantine--sticky__top" />
    <ObservatoryError v-if="statsError" :error="statsError" />
    <template v-if="stats">
      <ObservatoryWarnings :warnings="stats.notes.warnings" />
      <ObservatoryNumbers
        :canteensCount="stats.canteenCount"
        :canteensDescription="stats.notes.canteenCountDescription"
        :teledeclarationsCount="stats.teledeclarationsCount"
        class="fr-mb-3w"
      />
      <template v-if="stats.egalimPercent !== null">
        <ObservatoryPurchases :stats="stats" />
        <ObservatoryCanteens :stats="stats" />
      </template>
      <DsfrHighlight v-else :text="stats.notes.campaignInfo" class="fr-col-12 fr-col-md-8 fr-ml-0" />
    </template>
    <pre>{{ stats }}</pre>
  </section>
</template>

<style lang="scss">
.observatoire {
  &__results {
    &::before {
      z-index: -1;
      content: "";
      background-color: var(--background-alt-blue-france);
      position: absolute;
      top: 0;
      left: calc((100vw - 100%) / 2 * -1);
      width: 100vw;
      height: 100%;
    }
  }
}
</style>
