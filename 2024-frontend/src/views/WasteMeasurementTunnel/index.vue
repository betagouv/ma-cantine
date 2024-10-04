<script setup>
import WasteMeasurementSteps from "./WasteMeasurementSteps/index.vue"
import { computed, ref, watch, onMounted, provide, reactive } from "vue"
import { useRouter } from "vue-router"
import { BadRequestError } from "@/utils"

import { useRootStore } from "@/stores/root"
const store = useRootStore()

const props = defineProps(["canteenUrlComponent", "id", "étape"])

const canteenId = props.canteenUrlComponent.split("--")[0] // more globalised way of doing this?

const originalPayload = reactive({})
const dataIsReady = ref(!props.id)
provide("originalPayload", originalPayload)

onMounted(() => {
  if (props.id) {
    fetch(`/api/v1/canteens/${canteenId}/wasteMeasurements/${props.id}`)
      .then((response) => response.json())
      .then((body) => {
        Object.assign(originalPayload, body)
        dataIsReady.value = true
      })
  }
})

let steps = ref([])
const stepTitles = computed(() => steps.value.map((s) => s.title))
const stepIdx = computed(() => {
  let idx = steps.value.findIndex((s) => s.urlSlug === props.étape)
  return idx === -1 ? 0 : idx
})
const currentStep = computed(() => stepIdx.value + 1)
const step = computed(() => steps.value[stepIdx.value] || {})
const nextStep = computed(() => (stepIdx.value < steps.value.length - 1 ? steps.value[stepIdx.value + 1] : null))
const previousStep = computed(() => (stepIdx.value > 0 ? steps.value[stepIdx.value - 1] : null))

const updateSteps = (tunnelSteps) => {
  steps.value = tunnelSteps
}

const continueActionText = computed(() => {
  const onSynthesisView = step.value?.isSynthesis
  if (onSynthesisView) return "Passer à l'onglet suivant"
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
  if (!formIsValid()) {
    store.notifyRequiredFieldsError()
    return
  }
  return saveDiagnostic()
    .then((response) => {
      if (nextStep.value) {
        const nextRoute = { query: { étape: nextStep.value.urlSlug } }
        if (!props.id && response.id)
          nextRoute.params = { id: response.id, canteenUrlComponent: props.canteenUrlComponent }
        router.push(nextRoute)
        stepWrapper.value.scrollTop = 0
        Object.assign(originalPayload, hotPayload)
      } else {
        router.push({ name: "WasteMeasurements" })
      }
    })
    .catch(handleServerError)
}

const navigateBack = () => {
  router.push({ query: { étape: previousStep.value.urlSlug } })
  stepWrapper.value.scrollTop = 0
}

const goBack = () => {
  if (!previousStep.value) return
  // allow going back without validation if payload is empty, don't need to save
  if (Object.keys(hotPayload).length === 0) {
    navigateBack()
    return
  }
  if (!formIsValid()) return
  saveDiagnostic()
    .then(navigateBack)
    .catch(handleServerError)
}

const saveAndQuit = () => {
  if (!formIsValid()) return
  saveDiagnostic()
    .then(() => {
      router.push({ name: "WasteMeasurements" })
    })
    .catch(handleServerError)
}

let v$
const updateVuelidate = (vuelidateObj) => {
  v$ = vuelidateObj
}

let hotPayload = {}
const updatePayloadFromChild = (childPayload) => {
  if (!v$) {
    console.error("No vuelidate object")
    return
  }
  Object.assign(hotPayload, childPayload)
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

const saveDiagnostic = () => {
  if (!props.id) {
    return store.createWasteMeasurement(canteenId, hotPayload)
  }
  return store.updateWasteMeasurement(canteenId, props.id, hotPayload)
}

watch(props, () => {
  v$.value.$reset()
  hotPayload = {}
})
</script>

<template>
  <div class="tunnel">
    <div class="fr-container fr-pt-1w">
      <div class="measures fr-grid-row fr-grid-row--middle fr-py-2w">
        <div v-if="step" class="quit">
          <DsfrButton
            :label="step.isSynthesis ? 'Quitter' : 'Sauvegarder et quitter'"
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
      <DsfrStepper :steps="stepTitles" :currentStep />
    </div>
    <div class="body" ref="stepWrapper">
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
      <!-- Synthesis: content to go here. General styling to be applied too. -->
    </div>
    <div class="footer">
      <div class="content fr-container fr-grid-row fr-grid-row--right fr-p-2w fr-pr-8w">
        <!-- Synthesis: next tunnel name to go here. Check that continueActionText is correctly applied. -->
        <DsfrButton v-if="step.isSynthesis" label="Modifier" tertiary no-outline />
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
