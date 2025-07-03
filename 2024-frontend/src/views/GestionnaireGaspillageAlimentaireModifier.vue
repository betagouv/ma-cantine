<script setup>
import { computed, ref, watch, onMounted, provide, reactive } from "vue"
import { useRouter } from "vue-router"
import WasteMeasurementSteps from "@/components/WasteMeasurementSteps/index.vue"
import WasteSummary from "@/components/WasteSummary.vue"
import { BadRequestError } from "@/utils"
import { useRoute } from "vue-router"

import { useRootStore } from "@/stores/root"
const store = useRootStore()
const route = useRoute()

const props = defineProps(["canteenUrlComponent", "id", "étape"])

const canteenId = props.canteenUrlComponent.split("--")[0] // more globalised way of doing this?

const originalPayload = reactive({})
let canteen = ref({})
const dataIsReady = ref(!props.id)
provide("originalPayload", originalPayload)
provide("canteen", canteen)

onMounted(() => {
  if (props.id) {
    fetch(`/api/v1/canteens/${canteenId}/wasteMeasurements/${props.id}`)
      .then((response) => response.json())
      .then((body) => {
        Object.assign(originalPayload, body)
        dataIsReady.value = true
      })
  }
  store.fetchCanteen(canteenId).then((response) => (canteen.value = response))
})

let steps = ref([])
let allSteps = ref([]) // steps + synthesis, which we don't want in the stepper count UI
const stepTitles = computed(() => steps.value.map((s) => s.title))
const stepIdx = computed(() => {
  let idx = allSteps.value.findIndex((s) => s.urlSlug === props.étape)
  return idx === -1 ? 0 : idx
})
const currentStep = computed(() => stepIdx.value + 1)
const step = computed(() => allSteps.value[stepIdx.value] || {})
const nextStep = computed(() => (stepIdx.value < allSteps.value.length - 1 ? allSteps.value[stepIdx.value + 1] : null))
const previousStep = computed(() => (stepIdx.value > 0 ? allSteps.value[stepIdx.value - 1] : null))

const updateSteps = (tunnelSteps) => {
  steps.value = tunnelSteps
  allSteps.value = tunnelSteps.concat([
    {
      isSynthesis: true,
      urlSlug: "complet",
      title: "Synthèse",
    },
  ])
}

const continueActionText = computed(() => {
  const onSynthesisView = step.value?.isSynthesis
  if (onSynthesisView) return "Terminer"
  const nextIsSynthesis = nextStep.value?.isSynthesis
  if (nextIsSynthesis) return "Voir la synthèse"
  return "Sauvegarder et continuer"
})

const router = useRouter()

const stepWrapper = ref(null)

const formIsValid = () => {
  v$.value.$validate()
  return !v$.value.$invalid
}

const continueAction = () => {
  store.removeNotifications()
  if (step.value.isSynthesis) {
    quit()
    return
  }
  if (!formIsValid()) {
    store.notifyRequiredFieldsError()
    return
  }
  return saveDiagnostic()
    .then((response) => {
      const nextRoute = { query: { étape: nextStep.value.urlSlug } }
      if (isNew.value && response.id)
        nextRoute.params = { id: response.id, canteenUrlComponent: props.canteenUrlComponent }
      router.push(nextRoute)
      scrollTop()
      Object.assign(originalPayload, hotPayload.value)
    })
    .catch(handleServerError)
}

const navigateBack = () => {
  store.removeNotifications()
  router.push({ query: { étape: previousStep.value.urlSlug } })
  scrollTop()
}

const goBack = () => {
  if (!previousStep.value) return
  if (!hasChanges.value) {
    navigateBack()
    return
  }
  if (!formIsValid()) return
  saveDiagnostic()
    .then(navigateBack)
    .catch(handleServerError)
}

const goToFirstStep = () => {
  router.push({ query: { étape: steps.value[0].urlSlug } })
  scrollTop()
}

const scrollTop = () => {
  if (stepWrapper.value) stepWrapper.value.scrollTop = 0
}

const hasChanges = computed(() => {
  const relevantKeys = Object.keys(hotPayload.value)
  return relevantKeys.some((key) => hotPayload.value[key] !== originalPayload[key])
})
const saveAndQuit = () => {
  if (!hasChanges.value) quit()
  if (!formIsValid()) return
  saveDiagnostic()
    .then(quit)
    .catch(handleServerError)
}

const returnHref = ref(route.query?.return)

const quit = () => {
  if (returnHref.value) document.location.href = returnHref.value
  else router.push({ name: "GestionnaireGaspillageAlimentaire" })
}

let v$
const updateVuelidate = (vuelidateObj) => {
  v$ = vuelidateObj
}

let hotPayload = ref({})
const updatePayloadFromChild = (childPayload) => {
  if (!v$) {
    console.error("No vuelidate object")
    return
  }
  Object.assign(hotPayload.value, childPayload)
}

const handleServerError = (error) => {
  if (error instanceof BadRequestError) {
    return error.jsonPromise
      .then((errorDetail) => {
        const messages = Object.values(errorDetail)
        const message = messages && messages.length ? messages[0] : []
        store.notify({ message: message[0], status: "error" })
      })
      .catch(store.notifyServerError)
  }
  store.notifyServerError(error)
}

const isNew = computed(() => !props.id)

const saveDiagnostic = () => {
  if (isNew.value) {
    return store.createWasteMeasurement(canteenId, hotPayload.value)
  }
  return store.updateWasteMeasurement(canteenId, props.id, hotPayload.value)
}

watch(props, () => {
  v$.value.$reset()
  hotPayload.value = {}
})
</script>

<template>
  <div class="tunnel">
    <div class="fr-container fr-pt-1w">
      <div class="measures fr-grid-row fr-grid-row--middle fr-py-2w">
        <div v-if="step" class="quit">
          <DsfrButton
            v-if="step.isSynthesis || (stepIdx === 0 && isNew)"
            label="Quitter"
            @click="quit"
            icon="fr-icon-close-line"
            icon-right
            size="sm"
            tertiary
            no-outline
            class="fr-mr-n1w"
          />
          <DsfrButton
            v-else
            label="Sauvegarder et quitter"
            @click="saveAndQuit"
            icon="fr-icon-close-line"
            icon-right
            size="sm"
            tertiary
            no-outline
            class="fr-mr-n1w"
          />
        </div>
      </div>
      <DsfrStepper v-if="!step.isSynthesis" :steps="stepTitles" :currentStep />
    </div>
    <div v-if="step.isSynthesis" class="body synthesis">
      <div class="wrapper fr-container">
        <WasteSummary v-if="dataIsReady" :measurement="originalPayload" />
      </div>
    </div>
    <div v-else class="body" ref="stepWrapper">
      <div class="step fr-container">
        <div class="fr-py-1w">
          <WasteMeasurementSteps
            :stepUrlSlug="step.urlSlug"
            @update-steps="updateSteps"
            @provide-vuelidate="updateVuelidate"
            @update-payload="updatePayloadFromChild"
            v-if="dataIsReady"
          />
        </div>
      </div>
    </div>
    <div class="footer">
      <div class="content fr-container fr-grid-row fr-grid-row--right fr-p-2w fr-pr-8w">
        <DsfrButton v-if="step.isSynthesis" label="Modifier" tertiary no-outline @click="goToFirstStep" />
        <DsfrButton
          v-else
          label="Revenir à l'étape précédente"
          @click="goBack"
          tertiary
          no-outline
          :disabled="!previousStep"
        />
        <DsfrButton :label="continueActionText" @click="continueAction" class="fr-ml-1w" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.tunnel {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.tunnel,
.tunnel .footer {
  width: 100%;
  background-color: #f5f5fe;
}
.tunnel .body {
  overflow-y: scroll;
  overflow-x: hidden;
  background: #fff;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.tunnel .synthesis {
  background: unset;
}
.tunnel .synthesis .wrapper {
  margin-left: auto;
  margin-right: auto;
  height: 100%;
  width: 100%;
}
.step {
  max-height: 100%;
}
.header-icon {
  border-right: #e5e5e5 solid 1px;
  color: var(--blue-france-850-200);
}
.current-tab-icon {
  color: var(--blue-france-sun-113-625);
}
.measures {
  flex-wrap: nowrap;
}
.measure-title {
  text-transform: uppercase;
  font-weight: bold;
  color: var(--grey-425-625);
}
.quit {
  text-align: right;
  flex-grow: 1;
}
</style>
