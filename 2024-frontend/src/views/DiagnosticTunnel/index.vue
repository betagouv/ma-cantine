<script setup>
import keyMeasures from "@/data/key-measures.json"
import WasteMeasureSteps from "./WasteMeasureSteps/index.vue"
import { computed, ref, watch, onMounted, provide, reactive } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"

const store = useRootStore()

const props = defineProps(["canteenUrlComponent", "id", "étape"])

const canteenId = props.canteenUrlComponent.split("--")[0] // more globalised way of doing this?

// move this logic to a new file to save the skeleton of the tunnel for future Vue3 migration
// but having the idea of this tunnel as completely separate
const measureId = "gaspillage-alimentaire"
const measure = keyMeasures.find((measure) => measure.id === measureId)

const originalPayload = reactive({})
provide("originalPayload", originalPayload)

onMounted(() => {})

const tunnels = [
  ...keyMeasures.map((km) => ({
    id: km.id,
    title: km.title,
    shortTitle: km.shortTitle,
    icon: km.mdiIcon,
    backendField: km.progressField,
  })),
]

const tunnelComponents = {
  "gaspillage-alimentaire": WasteMeasureSteps,
}

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
  if (!formIsValid()) return
  saveDiagnostic()
    .then((response) => {
      if (nextStep.value) {
        const nextRoute = { query: { étape: nextStep.value.urlSlug } }
        if (!props.id && response.id)
          nextRoute.params = { id: response.id, canteenUrlComponent: props.canteenUrlComponent }
        router.push(nextRoute)
        stepWrapper.value.scrollTop = 0
        Object.assign(originalPayload, hotPayload)
      }
    })
    .catch((e) => {
      console.log(e)
      // TODO: show message from backend to user
    })
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
    .catch(() => {}) // Empty handler bc we handle the backend error on saveDiagnostic
}

const saveAndQuit = () => {
  if (!formIsValid()) return
  saveDiagnostic()
    .then(() => {
      router.push({ name: "MyProgress" })
    })
    .catch((e) => {
      console.error(e)
    }) // Empty handler bc we handle the backend error on saveDiagnostic
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

const saveDiagnostic = () => {
  if (!props.id) {
    return store.actions.createWasteMeasurement(canteenId, hotPayload)
  }
  return Promise.resolve()
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
        <div class="fr-col-12 fr-col-sm-8 fr-hidden fr-unhidden-sm">
          <div class="fr-grid-row fr-ml-n2w">
            <div
              v-for="tunnel in tunnels"
              :key="tunnel.id"
              class="fr-px-2w header-icon fr-grid-row fr-grid-row--middle"
            >
              <div v-if="tunnel.id === measure.id" class="fr-grid-row fr-grid-row--middle">
                <component :is="tunnel.icon" class="fr-mb-1v fr-mr-1w current-tab-icon" />
                <p class="measure-title fr-text--xs fr-mb-0">
                  {{ tunnel.shortTitle }}
                </p>
              </div>
              <div v-else>
                <component
                  :is="tunnel.icon"
                  fillColor="#ff0000"
                  :title="tunnel.shortTitle"
                  aria-hidden="false"
                  role="img"
                />
              </div>
            </div>
          </div>
        </div>
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
          <component
            :is="tunnelComponents[measureId]"
            :stepUrlSlug="step.urlSlug"
            @update-steps="updateSteps"
            @provide-vuelidate="updateVuelidate"
            @update-payload="updatePayloadFromChild"
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
