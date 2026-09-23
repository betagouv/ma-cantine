<script setup>
import { computed, ref } from "vue"
import { storeToRefs } from "pinia"
import { useRoute, useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import TunnelTeledeclarationTopNav from "@/components/TunnelTeledeclarationTopNav.vue"
import TunnelTeledeclarationSidebar from "@/components/TunnelTeledeclarationSidebar.vue"
import TunnelTeledeclarationModalErrors from "@/components/TunnelTeledeclarationModalErrors.vue"

const route = useRoute()
const router = useRouter()
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

/* Modal */
const showModal = ref(false)
const modalLink = ref("")
const modalErrors = ref([])
const displayModal = (errors, page) => {
  showModal.value = true
  modalErrors.value = errors
  modalLink.value = page
}

/* Redirect */
const goTo = (page) => {
  showModal.value = false
  router.push({ name: page })
}
</script>
<template>
  <div v-if="canteenInformations" class="ma-cantine--sticky__container ma-cantine--stick-to-footer">
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
        <TunnelTeledeclarationSidebar :canteen="canteenInformations" :nav="route.meta.nav" :active="currentRoute" />
      </div>
      <div class="fr-col-12 fr-col-md-9 fr-pl-0 fr-pl-md-4w">
        <TunnelTeledeclarationTopNav @errors="displayModal" />
        <div class="fr-mt-2w">
          <DsfrStepper v-if="hasStepper" :title="routeTitle" :steps="steps" :current-step="stepIndex" />
          <h1 v-else>{{ routeTitle }}</h1>
          <RouterView />
        </div>
      </div>
    </div>
    <TunnelTeledeclarationModalErrors
      :opened="showModal"
      :errors="modalErrors"
      @close="showModal = false"
      @continue="goTo(modalLink)"
    />
  </div>
</template>
