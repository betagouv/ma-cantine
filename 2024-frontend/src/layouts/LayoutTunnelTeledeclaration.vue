<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import TunnelTeledeclarationTopNav from "@/components/TunnelTeledeclarationTopNav.vue"
import TunnelTeledeclarationSidebar from "@/components/TunnelTeledeclarationSidebar.vue"
import TunnelTeledeclarationModalErrors from "@/components/TunnelTeledeclarationModalErrors.vue"
import TunnelTeledeclarationModalQuit from "@/components/TunnelTeledeclarationModalQuit.vue"

const route = useRoute()
const router = useRouter()
const currentRoute = computed(() => route.name)
const hideTopNav = computed(() => route.meta.hideTopNav)

/* Content */
const routeTitle = computed(() => route.meta.title)
const hasStepper = computed(() => route.meta.stepper && route.meta.stepper !== "" && route.meta.stepper !== undefined)
const routerSteps = computed(() => hasStepper.value ? route.meta.nav[route.meta.stepper] : [] )
const steps = computed(() => routerSteps.value.map((step) => step.title))
const stepIndex = computed(() => routerSteps.value.findIndex((step) => step.to.name === currentRoute.value) + 1)

/* Store */
const canteenStore = useStoreCanteen()
const { canteenInformations } = storeToRefs(canteenStore)
const teledeclarationStore = useStoreTeledeclaration()
const { isTeledeclared } = storeToRefs(teledeclarationStore)
const purchaseSummaryStore = useStorePurchaseSummary()

/* Saisie automatique */
const checkRedirect = (page) => {
  const isSaisie = currentRoute.value === "GestionnaireTunnelApproSaisie"
  const hasSelectAutofill = teledeclarationStore.hasSelectAutofill
  const isNotGeneratedFromPurchasesYet = !teledeclarationStore.diagnostic?.generatedFromPurchases
  const goToNextPage = page === route.meta.next
  const autofillRedirect = isSaisie && hasSelectAutofill && isNotGeneratedFromPurchasesYet && goToNextPage
  if (!autofillRedirect) return page
  return purchaseSummaryStore.hasPurchaseLocal ? "GestionnaireTunnelApproLocalCircuitCourt" : "GestionnaireTunnelApproRecapitulatif"
}

/* Save */
const save = async (page) => {
  const pageToGo = checkRedirect(page)
  teledeclarationStore.markPageAsVisited(route.meta.slug)
  const response = await teledeclarationStore.saveDiagnostic(route.meta.volet)
  if (response.status === "error") displayErrors(pageToGo)
  else checkDiagnostic(pageToGo)
}

/* Errors */
const checkDiagnostic = async (page) => {
  const check = await teledeclarationStore.checkDiagnosticSteps()
  if (check.isClean) goTo(page)
  else displayErrors(page)
}

const displayErrors = (page) => {
  const pageErrors = teledeclarationStore.getErrorsPage(route.name, canteenInformations.value.isGroupe)
  if (pageErrors.length > 0) displayModal(pageErrors, page)
  else goTo(page)
}

/* Modal */
const showModal = ref(false)
const modalLink = ref("")
const modalErrors = ref([])

const displayModal = (errors, page) => {
  showModal.value = true
  modalErrors.value = errors
  modalLink.value = page
}

/* Quit tunnel with unsaved data */
const showQuitModal = ref(false)
const quitRoute = ref(null)
const quitConfirmed = ref(false)

const quitBrowser = (event) => {
  if (!teledeclarationStore.hasDiagnostic || teledeclarationStore.isSaved) return
  event.preventDefault()
  event.returnValue = ""
}

const quitTunnel = (to) => {
  const canQuit = quitConfirmed.value || !teledeclarationStore.hasDiagnostic || teledeclarationStore.isSaved
  if (!canQuit) {
    quitRoute.value = to.fullPath
    showQuitModal.value = true
  }
  return canQuit
}

const quit = () => {
  showQuitModal.value = false
  quitConfirmed.value = true
  teledeclarationStore.refreshStore()
  router.push(quitRoute.value)
}

onMounted(() => window.addEventListener("beforeunload", quitBrowser))
onBeforeUnmount(() => window.removeEventListener("beforeunload", quitBrowser))
onBeforeRouteLeave(quitTunnel)

/* Navigation */
const goTo = (page) => {
  showModal.value = false
  router.push({ name: page })
}
</script>
<template>
  <div v-if="canteenInformations" class="ma-cantine--sticky__container ma-cantine--stick-to-footer">
    <div class="fr-grid-row">
      <div class="fr-col-12 fr-col-md-3 fr-hidden fr-unhidden-md">
        <TunnelTeledeclarationSidebar :canteen="canteenInformations" :nav="route.meta.nav" :active="currentRoute" @save="save" :displayTeledeclaredBadge="isTeledeclared" />
      </div>
      <div class="fr-col-12 fr-col-md-9">
        <TunnelTeledeclarationTopNav v-if="!hideTopNav" @save="save" />
        <div class="fr-mt-2w fr-pl-0 fr-pl-md-4w">
          <DsfrStepper v-if="hasStepper" :title="routeTitle" :steps="steps" :current-step="stepIndex" />
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
    <TunnelTeledeclarationModalQuit
      :opened="showQuitModal"
      @close="showQuitModal = false"
      @continue="quit"
    />
  </div>
</template>
