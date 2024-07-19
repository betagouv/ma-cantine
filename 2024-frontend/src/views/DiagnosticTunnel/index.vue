<script setup>
import keyMeasures from "@/data/key-measures.json"
import WasteMeasureSteps from "./WasteMeasureSteps/index.vue"

const props = defineProps(["canteenUrlComponent", "year", "measureId", "étape"])

const measure = keyMeasures.find((measure) => measure.id === props.measureId)

// TODO: get steps from child tunnel component
const steps = [
  {
    id: "example",
    title: "Step 1",
  },
  {
    id: "test",
    title: "Step 2",
  },
]
const stepTitles = steps.map((s) => s.title)
const stepIdx = steps.findIndex((s) => s.id === props.étape)
const currentStep = stepIdx + 1
const step = steps[stepIdx]

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
        <component :is="tunnelComponents[props.measureId]" />
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
        <DsfrButton v-else label="Revenir à l'étape précédente" tertiary no-outline :disabled="currentStep === 1" />
        <DsfrButton label="Sauvegarder et continuer" class="fr-ml-1w" />
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
