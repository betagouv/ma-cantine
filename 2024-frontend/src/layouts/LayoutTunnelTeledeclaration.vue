<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
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

/* Store */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)

</script>
<template>
  <div v-if="canteenInformations" class="ma-cantine--sticky__container ma-cantine--stick-to-footer">
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
        <TunnelTeledeclarationSidebar :canteen="canteenInformations" :nav="route.meta.nav" :active="currentRoute" />
      </div>
      <div class="fr-col-12 fr-col-md-9 fr-pl-0 fr-pl-md-4w">
        <TunnelTeledeclarationTopNav class="ma-cantine--sticky__top" />
        <div class="fr-mt-2w">
          <DsfrStepper v-if="hasStepper" :title="routeTitle" :steps="steps" :current-step="stepIndex" />
          <h1 v-else>{{ routeTitle }}</h1>
          <RouterView />
        </div>
      </div>
    </div>
  </div>
</template>
