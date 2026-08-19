<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import { useStoreDiagnostic } from "@/stores/diagnostic.js"
import urlService from "@/services/urls.js"
import AppLoader from "@/components/AppLoader.vue"
import TunnelTeledeclarationTopNav from "@/components/TunnelTeledeclarationTopNav.vue"
import TunnelTeledeclarationSidebar from "@/components/TunnelTeledeclarationSidebar.vue"

const route = useRoute()
const currentRoute = computed(() => route.name)

/* Content */
const routeTitle = computed(() => route.meta.title)
const hasStepper = computed(() => route.meta.stepper && route.meta.stepper !== "" && route.meta.stepper !== undefined)
const routerSteps = computed(() => hasStepper.value ? route.meta.nav[route.meta.stepper] : [] )
const steps = computed(() => routerSteps.value.map((step) => step.title))
const stepIndex = computed(() => routerSteps.value.findIndex((step) => step.to.name === currentRoute.value) + 1)
const hideTopBar = computed(() => route.meta.hideTopBar)

/* Store */
const canteenUrlId = computed(() => urlService.getCanteenId(route.params.canteenUrlComponent))
const isLoading = ref(false)
const canteenStore = useStoreCanteen()
const diagnosticStore = useStoreDiagnostic()
const { canteenInformations } = storeToRefs(canteenStore)
const loadStores = async () => {
  if (!canteenInformations.value || canteenInformations.value.id != canteenUrlId.value) {
    isLoading.value = true
    await Promise.all([
      canteenStore.initStore(canteenUrlId.value),
      diagnosticStore.initStore(canteenUrlId.value),
    ])
    isLoading.value = false
  }
}
onMounted(() => loadStores())
onUnmounted(() => {
  canteenStore.deleteStore()
  diagnosticStore.deleteStore()
})
watch(canteenUrlId, () => loadStores())
</script>
<template>
  <AppLoader v-if="isLoading || !canteenInformations" />
  <div v-else class="ma-cantine--sticky__container ma-cantine--stick-to-footer">
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
        <TunnelTeledeclarationSidebar :canteen="canteenInformations" :nav="route.meta.nav" :active="currentRoute" />
      </div>
      <div class="fr-col-12 fr-col-md-9 fr-pl-0 fr-pl-md-4w">
        <TunnelTeledeclarationTopNav v-if="!hideTopBar" class="ma-cantine--sticky__top" />
        <div class="fr-mt-2w">
          <DsfrStepper v-if="hasStepper" :title="routeTitle" :steps="steps" :current-step="stepIndex" />
          <h1 v-else>{{ routeTitle }}</h1>
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>
