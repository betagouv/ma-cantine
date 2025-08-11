<script setup>
import { onMounted, ref, useTemplateRef, watchEffect } from "vue"
import { useRouter } from "vue-router"
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
import ObservatoryShare from "@/components/ObservatoryShare.vue"
import AppJeDonneMonAvis from "@/components/AppJeDonneMonAvis.vue"

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

/* Router */
const router = useRouter()
const hasMount = ref(false)
const updateRouter = () => {
  const queryParam = storeFilters.getQueryParams()
  router.replace({ query: queryParam })
}
onMounted(() => {
  hasMount.value = true
})

/* Watch filters */
watchEffect(async () => {
  updateRouter()
  resetStatsValue()
  const newStats = await statisticsService.getStatistics(filtersParams)
  if (!newStats) setStatsError()
  else stats.value = newStats
  if (hasMount.value) updateRouter()
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
        <ObservatoryPurchases :stats="stats" class="fr-card fr-mb-4w fr-p-5w fr-px-md-6w fr-pt-md-8w fr-pb-md-6w" />
        <ObservatoryCanteens :stats="stats" class="fr-card fr-p-5w fr-px-md-6w fr-pt-md-8w fr-pb-md-6w" />
      </template>
      <DsfrHighlight v-else :text="stats.notes.campaignInfo" class="fr-col-12 fr-col-md-8 fr-ml-0" />
    </template>
    <ObservatoryShare v-if="!statsError" />
  </section>
  <AppJeDonneMonAvis url="https://jedonnemonavis.numerique.gouv.fr/Demarches/3661?button=3940">
    <p class="fr-mb-0">
      Qu'avez-vous penser de la page Observatoire ?
      <br />
      Avez-vous trouvé toutes les informations que vous cherchiez ?
    </p>
  </AppJeDonneMonAvis>
</template>

<style lang="scss">
.observatoire {
  &__results {
    $marginLeft: calc((100vw - 100%) / 2);

    &::before {
      z-index: -1;
      content: "";
      background-color: var(--background-alt-blue-france);
      position: absolute;
      top: 0;
      left: calc($marginLeft * -1);
      width: calc(100% + $marginLeft * 2);
      height: 100%;
    }
  }
}
</style>
