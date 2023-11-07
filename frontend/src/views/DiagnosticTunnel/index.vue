<template>
  <div class="text-left">
    <v-row class="header">
      <v-row class="mx-auto constrained pt-6">
        <v-col cols="9">
          <p class="fr-text-xs text-transform-uppercase mb-0">{{ measure.shortTitle }}</p>
        </v-col>
        <v-col class="text-right">
          <p class="mb-0">
            <router-link :to="quitLink">
              Quitter
              <v-icon color="primary" size="1rem" class="ml-0 mb-1">
                $close-line
              </v-icon>
            </router-link>
          </p>
        </v-col>
        <v-col v-if="step && !step.isSynthesis" cols="12">
          <div>
            <div class="fr-stepper">
              <h1 class="fr-stepper__title mb-4">
                <span class="fr-stepper__state">Étape {{ stepIdx + 1 }} sur {{ stepperStepTotal }}</span>
                {{ step.title }}
              </h1>
              <v-row
                class="fr-stepper__steps ma-0"
                :data-fr-current-step="stepIdx + 1"
                :data-fr-steps="stepperStepTotal"
              >
                <v-col v-for="(_, idx) in Array(stepperStepTotal)" :key="idx" :class="stepClass(idx)" />
              </v-row>
              <p v-if="nextStep" class="fr-stepper__details mt-4">
                <span class="font-weight-bold">Étape suivante :</span>
                {{ nextStep.title }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-row>
    <div v-if="diagnostic" class="mx-auto constrained pa-10">
      <component
        :is="`${measure.baseComponent}Steps`"
        :canteen="canteen"
        :diagnostic="diagnostic"
        :stepUrlSlug="stepUrlSlug"
        v-on:update-payload="updatePayload"
        v-on:update-steps="updateSteps"
      />
    </div>
    <v-row class="footer">
      <v-row class="mx-auto constrained">
        <v-col v-if="nextMeasureTitle" cols="5">
          <p class="fr-text-xs grey--text text--darken-2">
            Onglet suivant :
            <b>{{ nextMeasureTitle }}</b>
          </p>
        </v-col>
        <v-spacer />
        <v-col>
          <v-row class="py-10 align-center justify-end">
            <p v-if="step && step.isSynthesis" class="mb-0"><router-link :to="firstStepLink">Modifier</router-link></p>
            <p v-else class="mb-0">
              <router-link :to="previousStep ? previousStep.to : {}">
                Revenir à l'étape précédente
              </router-link>
            </p>
            <v-btn :disabled="!formIsValid" @click="continueAction" color="primary" class="ml-4">
              {{ continueActionText }}
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-row>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"
import QualityMeasureSteps from "./QualityMeasureSteps"
import WasteMeasureSteps from "./WasteMeasureSteps"

export default {
  name: "DiagnosticTunnel",
  props: {
    canteenUrlComponent: {
      type: String,
      required: true,
    },
    year: {
      required: true,
    },
    measureId: {
      type: String,
      required: true,
    },
  },
  components: { QualityMeasureSteps, WasteMeasureSteps },
  data() {
    return {
      formIsValid: false,
      canteen: null,
      diagnostic: null,
      payload: {},
      steps: [],
    }
  },
  computed: {
    canteenId() {
      return this.canteenUrlComponent.split("--")[0]
    },
    measure() {
      return keyMeasures.find((measure) => measure.id === this.measureId)
    },
    stepUrlSlug() {
      return this.$route.query.étape
    },
    stepIdx() {
      let idx = 0
      if (this.stepUrlSlug) {
        idx = this.steps.findIndex((step) => step.urlSlug === this.stepUrlSlug)
        idx = idx > -1 ? idx : 0
      }
      return idx
    },
    step() {
      return this.steps[this.stepIdx]
    },
    nextStep() {
      return this.stepIdx < this.steps.length - 1 ? this.steps[this.stepIdx + 1] : null
    },
    previousStep() {
      return this.stepIdx > 0 ? this.steps[this.stepIdx - 1] : null
    },
    continueActionText() {
      const returnToTable = this.step?.isFinal
      if (returnToTable) return "Retour au tableau de bord"
      const nextIsNewMeasure = this.step?.isSynthesis
      if (nextIsNewMeasure) return "Passer à l'onglet suivant"
      const nextIsSynthesis = this.nextStep?.isSynthesis
      if (nextIsSynthesis) return "Voir la synthèse"
      return "Sauvegarder et continuer"
    },
    nextMeasureTitle() {
      return this.nextStep?.measure?.title
    },
    quitLink() {
      return {
        name: "MyProgress",
        params: {
          canteenUrlComponent: this.canteenUrlComponent,
          year: this.year,
          measure: this.measureId,
        },
      }
    },
    firstStepLink() {
      return { query: { étape: this.steps[0].urlSlug } }
    },
    stepperStepTotal() {
      // we do not count the synthèse as a step, this assumes that all steps will include a final synthèse
      return this.steps.length - 1
    },
  },
  methods: {
    updateSteps(steps) {
      this.steps = steps
    },
    updatePayload({ payload, formIsValid }) {
      this.payload = payload
      this.formIsValid = formIsValid
    },
    fetchCanteen() {
      const id = this.canteenId
      return this.$store.dispatch("fetchCanteen", { id }).then((canteen) => {
        this.$set(this, "canteen", canteen)
      })
    },
    fetchDiagnostic() {
      if (!this.canteen) return
      this.diagnostic = this.canteen.diagnostics.find((d) => d.year === +this.year)
    },
    validateForm() {
      this.formIsValid = true
    },
    saveDiagnostic() {
      if (!this.canteen || !this.diagnostic) return Promise.reject()
      this.updateProgress()
      return this.$store
        .dispatch("updateDiagnostic", {
          canteenId: this.canteen.id,
          id: this.diagnostic.id,
          payload: this.payload,
        })
        .then(() => {
          // if the save is successful, make sure we are showing the up to date data
          Object.assign(this.diagnostic, this.payload)
        })
    },
    continueAction() {
      if (!this.formIsValid) return
      this.saveDiagnostic().then(() => {
        if (this.nextStep) {
          this.$router.push({ query: { étape: this.nextStep.urlSlug } })
        }
      })
    },
    updateProgress() {
      if (this.isSynthesis) this.payload.tunnelQuality = "COMPLETE"
      else if (this.step.isFinal) this.payload.tunnelComplete = true
      this.payload.tunnelQuality = this.step?.urlSlug
    },
    updatePageTitle() {
      document.title = `${this.step.title} - ${this.year} - ${this.canteen.name} - ${this.$store.state.pageTitleSuffix}`
    },
    replaceStepInUrlMaybe() {
      const url = this.$route.query.étape
      if (!url || url !== this.step?.urlSlug) {
        this.$router.replace(this.firstStepLink)
      }
    },
    stepClass(idx) {
      const margins = idx === 0 ? "mr-1" : idx === this.stepperStepTotal - 1 ? "ml-1" : "mx-1"
      return `${margins} mc-stepper__step ${idx <= this.stepIdx ? "completed" : "future"}`
    },
  },
  mounted() {
    this.fetchCanteen().then(() => this.fetchDiagnostic())
  },
  watch: {
    step(newStep) {
      this.replaceStepInUrlMaybe()
      if (newStep) this.updatePageTitle()
    },
  },
}
</script>

<style>
.header {
  background-color: #f5f5fe;
}
.footer {
  background-color: #f5f5fe;
}
/* DSFR STEPPER */
.fr-stepper {
  --title-spacing: 0;
  --text-spacing: 0;
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
}
.fr-stepper__title {
  --title-spacing: 0 0 0.75rem 0;
  --text-spacing: 0 0 0.75rem 0;
  color: #161616;
  /* color: var(--text-title-grey); */
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1.5rem;
}
.fr-stepper__state {
  --title-spacing: 0 0 0.25rem 0;
  --text-spacing: 0 0 0.25rem 0;
  color: #666;
  /* color: var(--text-mention-grey); */
  font-size: 0.875rem;
  font-weight: 400;
  line-height: 1.5rem;
}
.fr-stepper__state:after {
  content: "\a";
  line-height: 2rem;
  white-space: pre;
}
.fr-stepper__details {
  color: #666;
  /* color: var(--text-mention-grey); */
  font-size: 0.75rem;
  line-height: 1.25rem;
  margin-top: 0.75rem;
}
/* .fr-stepper__steps {
  height: 6px;
} */
.mc-stepper__step {
  height: 6px;
  padding: 0;
}
.mc-stepper__step.completed {
  background-color: #000091;
}
.mc-stepper__step.future {
  background-color: #eee;
}
</style>
