<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { onBeforeRouteLeave, useRoute, useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import canteenServices from "@/services/canteens"
import diagnosticServices from "@/services/diagnostics"
import TunnelTeledeclarationTopNav from "@/components/TunnelTeledeclarationTopNav.vue"
import TunnelTeledeclarationSidebar from "@/components/TunnelTeledeclarationSidebar.vue"
import TunnelTeledeclarationModalErrors from "@/components/TunnelTeledeclarationModalErrors.vue"
import TunnelTeledeclarationModalQuit from "@/components/TunnelTeledeclarationModalQuit.vue"

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
const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)

/* Save */
const save = async (page) => {
  teledeclarationStore.clearErrors()
  await teledeclarationStore.saveDiagnostic()
  const check = await checkIsFilled()
  if (check.isFilled) goTo(page)
  else checkErrors(check.errors, page)
}

/* Errors */
const checkErrors = async (errors, page) => {
  await teledeclarationStore.addErrorsFromCheck(errors)
  const pageErrors = teledeclarationStore.getErrorsPage(route.name, canteenInformations.value.isGroupe)
  if (pageErrors.length > 0) displayModal(pageErrors, page)
  else goTo(page)
}

const checkIsFilled = async () => {
  const canteenId = diagnostic.value.canteenId
  const diagnosticId = diagnostic.value.id
  const checkCanteen = await canteenServices.checkCanteen(canteenId)
  const checkDiagnostic = await diagnosticServices.checkDiagnostic(canteenId, diagnosticId)
  const isCanteenFilled = checkCanteen.isFilled && checkCanteen.errors.length === 0
  const isDiagnosticFilled = checkDiagnostic.isFilled && checkDiagnostic.errors.length === 0
  return { isFilled: isCanteenFilled && isDiagnosticFilled, errors: {...checkCanteen.errors, ...checkDiagnostic.errors} }
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
  if (quitConfirmed.value || !teledeclarationStore.hasDiagnostic || teledeclarationStore.isSaved) return true
  quitRoute.value = to.fullPath
  showQuitModal.value = true
  return false
}

const quit = () => {
  showQuitModal.value = false
  quitConfirmed.value = true
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
        <TunnelTeledeclarationSidebar :canteen="canteenInformations" :nav="route.meta.nav" :active="currentRoute" @save="save" />
      </div>
      <div class="fr-col-12 fr-col-md-9 fr-pl-0 fr-pl-md-4w">
        <TunnelTeledeclarationTopNav @save="save" />
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
    <TunnelTeledeclarationModalQuit
      :opened="showQuitModal"
      @close="showQuitModal = false"
      @continue="quit"
    />
  </div>
</template>
