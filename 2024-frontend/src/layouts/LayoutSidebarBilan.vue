<script setup>
import { useRoute } from "vue-router"
import { computedAsync } from "@vueuse/core"
import { computed } from "vue"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"

/* Route */
const route = useRoute()
const currentRoute = computed(() => route.name)

/* Header */
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const canteenInformation = computedAsync(async () => await canteenService.fetchCanteen(canteenId), false)
const canteenBadgeId = computed(() => canteenId ? `ID : ${canteenId}` : null)
const canteenBadgeSiret = computed(() => canteenInformation.value?.siret ? `SIRET : ${canteenInformation.value.siret}` : null)
const canteenBadgeSiren = computed(() => canteenInformation.value?.sirenUniteLegale ? `SIREN : ${canteenInformation.value.sirenUniteLegale}` : null)

/* Sidebar links */
const informationActive = computed(() => currentRoute.value === "GestionnaireBilanInformations")
const menuItems = [
  {
    text: "Mes informations",
    to: { name: "GestionnaireBilanInformations" },
    active: informationActive
  },
  {
    text: "Mes gestionnaires",
    to: { name: "" },
    active: false
  },
  {
    text: "Ma page publique",
    to: { name: "" },
    active: false
  },
  {
    text: "Toutes mes déclarations",
    to: { name: "" },
    active: false
  },
]
</script>

<template>
  <div>
    <h1>{{ canteenName }}</h1>
    <div class="ma-cantine--flex-start ma-cantine--flex-gap-1 fr-mb-4w fr-mb-md-0">
      <DsfrBadge v-if="canteenBadgeId" type="neutral" :label="canteenBadgeId" />
      <DsfrBadge v-if="canteenBadgeSiret" type="neutral" :label="canteenBadgeSiret" />
      <DsfrBadge v-if="canteenBadgeSiren" type="neutral" :label="canteenBadgeSiren" />
    </div>
    <div class="fr-grid-row fr-grid-row--top ma-cantine--sticky__container">
      <div class="fr-col-12 fr-col-md-3 ma-cantine--sticky__top fr-background-default--grey">
        <DsfrSideMenu :menu-items="menuItems" buttonLabel="Voir le menu"/>
      </div>
      <section class="fr-col-12 fr-col-md-9 fr-pt-3w">
        <slot></slot>
      </section>
    </div>
  </div>
</template>
