<script setup>
import keyMeasures from "@/data/key-measures.json"

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
</script>

<template>
  <!-- TODO: mobile view optimisations -->
  <!-- TODO: synthesis styling -->
  <div class="tunnel">
    <div class="fr-container fr-pt-2w">
      <div class="fr-grid-row fr-grid-row--middle">
        <!-- TODO: hide on xs -->
        <div class="fr-col-9">
          <div class="fr-grid-row fr-ml-n2w">
            <div
              v-for="tunnel in tunnels"
              :key="tunnel.id"
              class="fr-px-2w header-icon fr-grid-row fr-grid-row--middle"
            >
              <div v-if="tunnel.id === measure.id" class="fr-grid-row fr-grid-row--middle">
                <!-- TODO: proper colours (originally primary and primary lighten-4) -->
                <component :is="tunnel.icon" class="fr-mb-1v fr-mr-1v" />
                <!-- text-uppercase mb-0 grey--text text--darken-2 font-weight-bold -->
                <p class="tunnel-header-title fr-text--xs fr-mb-0">
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
        <div v-if="step" class="fr-col-3 quit">
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
      <div class="step fr-container fr-py-2w">
        <!-- TODO: setup steps in child folder -->
        <DsfrInput
          v-model="name"
          label="Nom"
          placeholder="Jean Dupont"
          label-visible
          required
          hint="Indiquez votre nom"
        />
      </div>
      <!-- TODO: setup synthesis -->
    </div>
    <div class="footer">
      <div class="content fr-container fr-grid-row fr-grid-row--right fr-p-2w">
        <!-- TODO: next tab text on synthesis view -->
        <!-- TODO: button functionalities -->
        <DsfrButton v-if="step.isSynthesis" label="Modifier" tertiary no-outline class="fr-mr-1w" />
        <DsfrButton
          v-else
          label="Revenir à l'étape précédente"
          tertiary
          no-outline
          :disabled="currentStep === 1"
          class="fr-mr-1w"
        />
        <DsfrButton label="Sauvegarder et continuer" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.tunnel {
  display: flex;
  flex-direction: column;
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
}
.tunnel .footer {
  position: absolute;
  bottom: 0;
}
.scroll {
  overflow-y: scroll;
  overflow-x: hidden;
}
.header-icon {
  border-right: #e5e5e5 solid 1px;
}
.tunnel-header-title {
  text-transform: uppercase;
  font-weight: bold;
}
.quit {
  text-align: right;
}
</style>
