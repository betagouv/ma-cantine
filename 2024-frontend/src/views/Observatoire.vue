<script setup>
import { ref, watchEffect, useTemplateRef } from "vue"
import { useStoreFilters } from "@/stores/filters"
import statisticsService from "@/services/statistics"
import ObservatoryHero from "@/components/ObservatoryHero.vue"
import ObservatoryFilters from "@/components/ObservatoryFilters.vue"
import ObservatoryResultsFilters from "@/components/ObservatoryResultsFilters.vue"

/* Back to filters */
const observatoryFilters = useTemplateRef("observatory-filters")
const scrollToFilters = () => {
  observatoryFilters.value.anchor.scrollIntoView({ behavior: "smooth" })
}

/* Get stats */
const storeFilters = useStoreFilters()
const filtersParams = storeFilters.getAll()
const stats = ref()
watchEffect(async () => {
  const newStats = await statisticsService.getStatistics(filtersParams)
  stats.value = newStats
})
</script>

<template>
  <ObservatoryHero />
  <ObservatoryFilters ref="observatory-filters" />
  <section class="observatoire__results ma-cantine--sticky__container fr-mt-4w fr-pb-4w">
    <ObservatoryResultsFilters @scrollToFilters="scrollToFilters()" class="ma-cantine--sticky__top" />
    <DsfrNotice
      class="fr-my-2w"
      title="Pour des raisons de confidentialité, les cantines des armées ne sont pas intégrées dans cet observatoire."
    />
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
