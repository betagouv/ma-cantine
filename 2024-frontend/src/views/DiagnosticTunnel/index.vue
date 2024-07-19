<script setup>
import keyMeasures from "@/data/key-measures.json"
// TODO: sort out **/index.vue imports so don't have to add index.vue
import WasteMeasureSteps from "./WasteMeasureSteps/index.vue"
import { computed, ref } from "vue"
import { useRouter } from "vue-router"

const props = defineProps(["canteenUrlComponent", "year", "measureId", "étape"])

const measure = keyMeasures.find((measure) => measure.id === props.measureId)

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

const saveDiagnostic = () => {
  // TODO
  return Promise.resolve()
}

const router = useRouter()

const continueAction = () => {
  // TODO
  // if (!this.formIsValid) return
  saveDiagnostic()
    .then(() => {
      if (nextStep.value) {
        router.push({ query: { étape: nextStep.value.urlSlug } })
        // TODO
        // $refs["stepWrapper"].scrollTop = 0
        // $refs["synthesisWrapper"].scrollTop = 0
        // } else if (isLastTunnel) {
        //   router.push({
        //     name: "MyProgress",
        //     params: { measure: "etablissement" },
        //   })
        // } else if (nextTunnel) {
        //   router.push({
        //     name: "MyProgress",
        //     params: { measure: nextTunnel.id },
        //   })
        // } else {
        //   router.push({
        //     name: "DashboardManager",
        //     params: {
        //       canteenUrlComponent: canteenUrlComponent,
        //     },
        //     query: {
        //       year: year,
        //     },
        //   })
      }
    })
    .catch(() => {}) // Empty handler bc we handle the backend error on saveDiagnostic
}

const goBack = () => {
  if (!previousStep.value) return
  // TODO: check if form is valid
  // if (!formIsValid) return
  saveDiagnostic()
    .then(() => {
      router.push({ query: { étape: previousStep.value.urlSlug } })
      // TODO: scroll to top of tunnel content
      // $refs["stepWrapper"].scrollTop = 0
    })
    .catch(() => {}) // Empty handler bc we handle the backend error on saveDiagnostic
}
</script>

<template>
  <!-- TODO: mobile view optimisations -->
  <!-- TODO: synthesis styling -->
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
        <!-- TODO: functionality -->
        <div v-if="step" class="quit">
          <DsfrButton
            :label="step.isSynthesis ? 'Quitter' : 'Sauvegarder et quitter'"
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
    <div class="body">
      <div class="step fr-container">
        <component :is="tunnelComponents[props.measureId]" :stepUrlSlug="step.urlSlug" @update-steps="updateSteps" />
        <!--
          :canteen="canteen"
          :diagnostic="diagnostic"
          :stepUrlSlug="stepUrlSlug"
          v-on:update-payload="updatePayload"
          v-on:tunnel-autofill="onTunnelAutofill"
          v-on:update-steps="updateSteps"
         -->
      </div>
      <!-- TODO: setup synthesis -->
    </div>
    <div class="footer">
      <div class="content fr-container fr-grid-row fr-grid-row--right fr-p-2w fr-pr-8w">
        <!-- TODO: next tab text on synthesis view -->
        <!-- TODO: button functionalities -->
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
.scroll {
  overflow-y: scroll;
  overflow-x: hidden;
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
