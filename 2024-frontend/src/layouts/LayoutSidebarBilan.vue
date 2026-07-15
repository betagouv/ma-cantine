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
const canteenIsGroupe = computed(() => canteenInformation.value?.productionType === "groupe")
const canteenBadgeId = computed(() => canteenId ? `ID : ${canteenId}` : null)
const canteenBadgeSiret = computed(() => canteenInformation.value?.siret ? `SIRET : ${canteenInformation.value.siret}` : null)
const canteenBadgeSiren = computed(() => canteenInformation.value?.sirenUniteLegale ? `SIREN : ${canteenInformation.value.sirenUniteLegale}` : null)
const canteenBadgeGroupe = computed(() => {
  if (!canteenIsGroupe.value) return null
  const nbRestaurants = canteenInformation.value?.satellitesCount
  return `Groupe : ${nbRestaurants} ${nbRestaurants > 1 ? "restaurants" : "restaurant"}`
})

/* Sidebar links */
const menuItems = computed(() =>  {
  const informationActive = currentRoute.value === "GestionnaireBilanInformations"
  const gestionnairesActive = currentRoute.value === "GestionnaireBilanGestionnaires"
  const pagePubliqueActive = currentRoute.value === "GestionnaireBilanPagePublique"
  const toutesTeledeclarationsActive = currentRoute.value === "GestionnaireBilanToutesTeledeclarations"
  const cantinesGroupeActive = currentRoute.value === "GestionnaireBilanCantinesGroupe"

  const informationPage = {
    text: canteenIsGroupe.value ? "Informations du groupe" : "Informations",
    to: { name: "GestionnaireBilanInformations" },
    active: informationActive
  }
  const gestionnairesPage = {
    text: "Gestionnaires",
    to: '/',
    active: gestionnairesActive
  }
  const cantinesGroupePage = {
    text: "Cantines du groupe",
    to: '/',
    active: cantinesGroupeActive
  }
  const pagePubliquePage = {
    text: "Page publique",
    to: '/',
    active: pagePubliqueActive
  }
  const teledeclarationsPage =  {
    text: "Toutes mes télédéclarations",
    to: { name: "" },
    active: toutesTeledeclarationsActive
  }

  // Dynamic links
  const pages = []
  pages.push(informationPage)
  pages.push(gestionnairesPage)
  if (canteenIsGroupe.value) pages.push(cantinesGroupePage)
  if (!canteenIsGroupe.value) pages.push(pagePubliquePage)
  pages.push(teledeclarationsPage)

  return pages
})
</script>

<template>
  <div class="layout-sidebar-bilan">
    <h1>{{ canteenName }}</h1>
    <div class="ma-cantine--flex-start ma-cantine--flex-gap-1 fr-mb-4w">
      <DsfrBadge v-if="canteenBadgeGroupe" type="info" :noIcon="true" :label="canteenBadgeGroupe" />
      <DsfrBadge v-if="canteenBadgeId" type="neutral" :label="canteenBadgeId" />
      <DsfrBadge v-if="canteenBadgeSiret" type="neutral" :label="canteenBadgeSiret" />
      <DsfrBadge v-if="canteenBadgeSiren" type="neutral" :label="canteenBadgeSiren" />
    </div>
    <div class="fr-grid-row fr-grid-row--top ma-cantine--sticky__container">
      <div class="layout-sidebar-bilan__sidebar-container fr-col-12 fr-col-md-3 ma-cantine--sticky__top fr-background-default--grey">
        <DsfrSideMenu :menu-items="menuItems" buttonLabel="Voir le menu"/>
      </div>
      <section class="fr-col-12 fr-col-md-9 fr-pt-1w">
        <slot></slot>
      </section>
    </div>
  </div>
</template>

<style lang="scss">
.layout-sidebar-bilan {
  &__sidebar-container {
    .fr-sidemenu__title {
      display: none !important;
    }
    .fr-sidemenu__inner {
      padding-right: 0 !important;
    }
  }
}
</style>
