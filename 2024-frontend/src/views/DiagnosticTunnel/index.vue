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
const currentStep = (steps.findIndex((s) => s.id === props.étape) || 0) + 1

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
  <div class="tunnel">
    <div class="fr-container fr-pt-2w">
      <div class="fr-grid-row">
        <!-- TODO: hide on xs -->
        <div class="fr-col-9 fr-grid-row fr-mx-n2w">
          <div v-for="tunnel in tunnels" :key="tunnel.id" class="fr-px-2w header-icon fr-grid-row fr-grid-row--middle">
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
        <!-- TODO: save and quit -->
        <!-- <v-col class="text-right py-0" v-if="step">
          <p class="mb-0">
            <v-btn
              text
              plain
              class="text-decoration-underline px-0"
              color="primary"
              @click="step.isSynthesis ? quit() : saveAndQuit()"
              :disabled="!formIsValid && !isSynthesis"
            >
              {{ step.isSynthesis ? "Quitter" : "Sauvegarder et quitter" }}
              <v-icon color="primary" size="1rem" class="ml-0 mb-1">
                $close-line
              </v-icon>
            </v-btn>
          </p>
        </v-col> -->
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
        <!-- TODO: previous step link -->
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
</style>
