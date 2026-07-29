<script setup>
import { useRoute } from "vue-router"
import { computedAsync } from "@vueuse/core"
import { computed } from "vue"
import { formatSiretOrSiren } from "@/utils"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"
import AppSeparator from "@/components/AppSeparator.vue"

/* Route */
const route = useRoute()
const currentRoute = computed(() => route.name)

/* Header */
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const canteenInformation = computedAsync(async () => await canteenService.fetchCanteen(canteenId), false)
const canteenIsGroupe = computed(() => canteenInformation.value?.productionType === "groupe")
const canteenBadgeId = computed(() => canteenId ? `ID : ${canteenId}` : null)
const canteenBadgeSiret = computed(() => canteenInformation.value?.siret ? `SIRET : ${formatSiretOrSiren(canteenInformation.value.siret)}` : null)
const canteenBadgeSiren = computed(() => canteenInformation.value?.sirenUniteLegale ? `SIREN : ${formatSiretOrSiren(canteenInformation.value.sirenUniteLegale)}` : null)
const canteenBadgeGroupe = computed(() => {
  if (!canteenIsGroupe.value) return null
  const nbRestaurants = canteenInformation.value?.satellitesCount
  return `Groupe : ${nbRestaurants} ${nbRestaurants > 1 ? "restaurants" : "restaurant"}`
})

/* Sidebar links */
const menuItems = computed(() =>  {
  const cantineActive = currentRoute.value === "GestionnaireCantine"
  const gestionnairesActive = currentRoute.value === "GestionnaireCantineGestionnaires"
  const pagePubliqueActive = currentRoute.value === "GestionnaireCantinePagePublique"
  const teledeclarationsActive = currentRoute.value === "GestionnaireCantineTeledeclarations"
  const cantinesGroupeActive = currentRoute.value === "GestionnaireCantineGroupe"

  const cantinePage = {
    text: canteenIsGroupe.value ? "Informations du groupe" : "Mes informations",
    to: { name: "GestionnaireCantine" },
    active: cantineActive
  }
  const gestionnairesPage = {
    text: canteenIsGroupe.value ? "Gestionnaires" : "Mes gestionnaires",
    to: { name: "GestionnaireCantineGestionnaires" },
    active: gestionnairesActive
  }
  const cantinesGroupePage = {
    text: "Cantines du groupe",
    to: { name: "GestionnaireCantineGroupe" },
    active: cantinesGroupeActive
  }
  const pagePubliquePage = {
    text: "Ma page publique",
    to: { name: "GestionnaireCantinePagePublique" },
    active: pagePubliqueActive
  }
  const teledeclarationsPage =  {
    text: "Toutes mes télédéclarations",
    to: { name: "GestionnaireCantineTeledeclarations" },
    active: teledeclarationsActive
  }

  // Dynamic links
  const pages = []
  pages.push(cantinePage)
  pages.push(gestionnairesPage)
  if (canteenIsGroupe.value) pages.push(cantinesGroupePage)
  if (!canteenIsGroupe.value) pages.push(pagePubliquePage)
  pages.push(teledeclarationsPage)

  return pages
})
</script>

<template>
  <div class="layout-sidebar-canteen">
    <h1>{{ canteenName }}</h1>
    <div class="ma-cantine--flex-start ma-cantine--flex-gap-1 fr-mb-4w">
      <DsfrBadge v-if="canteenBadgeGroupe" type="info" :noIcon="true" :label="canteenBadgeGroupe" />
      <DsfrBadge v-if="canteenBadgeId" type="neutral" :label="canteenBadgeId" />
      <DsfrBadge v-if="canteenBadgeSiret" type="neutral" :label="canteenBadgeSiret" />
      <DsfrBadge v-if="canteenBadgeSiren" type="neutral" :label="canteenBadgeSiren" />
    </div>
    <div class="fr-grid-row ma-cantine--sticky__container">
      <div class="layout-sidebar-canteen__sidebar-container fr-col-12 fr-col-md-3 fr-background-default--grey">
        <DsfrSideMenu :menu-items="menuItems" buttonLabel="Voir le menu" class="ma-cantine--sticky__top" titleTag="p" />
      </div>
      <section class="fr-col-12 fr-col-md-9 fr-pb-2w">
        <div class="ma-cantine--flex-between ma-cantine--flex-gap-1 fr-mt-2w fr-mt-md-0 fr-mb-2w fr-mb-md-0">
          <h2 class="fr-h3 fr-mb-0">
            <slot name="titleName" :canteenIsGroupe="canteenIsGroupe"></slot>
          </h2>
          <slot name="titleButton" :canteenIsGroupe="canteenIsGroupe"></slot>
        </div>
        <AppSeparator class="layout-sidebar-canteen__separator fr-mt-3w fr-mb-5w" />
        <slot name="content" :canteenInformation="canteenInformation" :canteenIsGroupe="canteenIsGroupe"></slot>
      </section>
    </div>
  </div>
</template>

<style lang="scss">
.layout-sidebar-canteen {
  &__separator {
    display: none;

    @media (min-width: 768px) {
      display: block;
    }
  }
  &__sidebar-container {
    .fr-sidemenu__title {
      display: none !important;
    }
    .fr-sidemenu__inner {
      padding-right: 0 !important;
      box-shadow: none !important;
    }
  }
}
</style>
