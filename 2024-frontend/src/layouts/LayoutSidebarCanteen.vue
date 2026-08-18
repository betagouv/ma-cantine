<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue"
import { useRoute, RouterView } from "vue-router"
import { storeToRefs } from "pinia"
import { useStoreCanteen } from "@/stores/canteen.js"
import urlService from "@/services/urls.js"
import AppLoader from "@/components/AppLoader.vue"
import AppLinkMailto from "@/components/AppLinkMailto.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import AppBadgeCanteen from "@/components/AppBadgeCanteen.vue"
import AppBadgeSiretSiren from "@/components/AppBadgeSiretSiren.vue"

/* Route */
const route = useRoute()
const currentRoute = computed(() => route.name)
const canteenUrlId = computed(() => urlService.getCanteenId(route.params.canteenUrlComponent))
const isLoading = ref(false)

/* Store */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const loadStore = async () => {
  if (!canteenInformations.value || canteenInformations.value.id != canteenUrlId.value) {
    isLoading.value = true
    await canteenStore.initStore(canteenUrlId.value)
    isLoading.value = false
  }
}
onMounted(() => loadStore())
onUnmounted(() => canteenStore.deleteStore())
watch(canteenUrlId, () => loadStore())

/* Sidebar links */
const currentYear = new Date().getFullYear()
const menuItems = computed(() =>  {
  const isGroupe = canteenInformations.value?.isGroupe
  const cantineActive = currentRoute.value === "GestionnaireCantine"
  const gestionnairesActive = currentRoute.value === "GestionnaireCantineGestionnaires"
  const pagePubliqueActive = currentRoute.value === "GestionnaireCantinePagePublique"
  const teledeclarationEnCoursActive = currentRoute.value === "GestionnaireCantineTeledeclarationEnCours"
  const teledeclarationsActive = currentRoute.value === "GestionnaireCantineTeledeclarations"
  const cantinesGroupeActive = currentRoute.value === "GestionnaireCantineGroupe"

  const cantinePage = {
    text: isGroupe ? "Informations du groupe" : "Informations de la cantine",
    to: { name: "GestionnaireCantine" },
    active: cantineActive
  }
  const gestionnairesPage = {
    text: isGroupe ? "Gestionnaires du groupe" : "Gestionnaires de la cantine",
    to: { name: "GestionnaireCantineGestionnaires" },
    active: gestionnairesActive
  }
  const cantinesGroupePage = {
    text: "Cantines du groupe",
    to: { name: "GestionnaireCantineGroupe" },
    active: cantinesGroupeActive
  }
  const pagePubliquePage = {
    text: "Page publique et affiche",
    to: { name: "GestionnaireCantinePagePublique" },
    active: pagePubliqueActive
  }
  const teledeclarationEnCoursPage = {
    text: isGroupe ? `Télédéclaration ${currentYear}` : `Ma télédéclaration ${currentYear}`,
    to: { name: "GestionnaireCantineTeledeclarationEnCours" },
    active: teledeclarationEnCoursActive
  }
  const teledeclarationsPage =  {
    text: "Toutes les télédéclarations",
    to: { name: "GestionnaireCantineTeledeclarations" },
    active: teledeclarationsActive
  }

  // Dynamic links
  const pages = []
  pages.push(cantinePage)
  pages.push(gestionnairesPage)
  if (isGroupe) pages.push(cantinesGroupePage)
  else pages.push(pagePubliquePage)
  pages.push(teledeclarationEnCoursPage)
  pages.push(teledeclarationsPage)

  return pages
})
</script>

<template>
  <AppLoader v-if="isLoading" />
  <div v-else-if="canteenInformations" class="layout-sidebar-canteen">
    <DsfrAlert title="La page établissement a évolué" type="info" class="fr-mb-4w">
      <p>
        Cette nouvelle version a été construite à partir de vos retours dans un souci de simplicité, de performance et de sécurité. <br/>
      </p>
      <p>
        IMPORTANT : l’environnement propre aux bilans (ex. « Mon bilan annuel ») sera intégré dans une seconde version courant l’automne. <br/>
        En attendant, retrouvez vos données via les justificatifs de télédéclaration, page <AppLinkRouter :to="{ name: 'GestionnaireCantineTeledeclarations', hash: '#sidebar-canteen-content' }" title="Toutes les télédéclarations" />.
      </p>
      <p>Pour toute remarque ou question : <AppLinkMailto /></p>
    </DsfrAlert>
    <h1>{{ canteenInformations.name }}</h1>
    <div class="ma-cantine--flex-start ma-cantine--flex-gap-1 fr-mb-4w">
      <AppBadgeCanteen :canteen="canteenInformations" />
      <DsfrBadge :label="`ID : ${canteenInformations.id}`" type="neutral" />
      <AppBadgeSiretSiren :canteen="canteenInformations" />
    </div>
    <div class="fr-grid-row ma-cantine--sticky__container">
      <div class="layout-sidebar-canteen__sidebar-container fr-col-12 fr-col-md-3 fr-background-default--grey">
        <DsfrSideMenu :menu-items="menuItems" buttonLabel="Voir le menu" class="ma-cantine--sticky__top" titleTag="p" />
      </div>
      <section id="sidebar-canteen-content" class="fr-col-12 fr-col-md-9 fr-pb-2w">
        <RouterView />
      </section>
    </div>
  </div>
</template>

<style lang="scss">
.layout-sidebar-canteen {
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
