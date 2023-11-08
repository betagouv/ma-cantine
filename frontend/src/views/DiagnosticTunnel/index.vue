<template>
  <div class="text-left">
    <v-row class="header">
      <v-row class="mx-auto constrained pt-6">
        <v-col cols="9">
          <p class="fr-text-xs text-transform-uppercase mb-0">{{ measure.shortTitle }}</p>
        </v-col>
        <v-col class="text-right">
          <p class="mb-0">
            <v-btn text plain class="text-decoration-underline" color="primary" @click="saveAndQuit">
              Sauvegarder et quitter
              <v-icon color="primary" size="1rem" class="ml-0 mb-1">
                $close-line
              </v-icon>
            </v-btn>
          </p>
        </v-col>
        <v-col v-if="step && !step.isSynthesis" cols="12">
          <p class="fr-text-sm">Étape {{ stepIdx + 1 }} sur {{ stepTotal }}</p>
          <h1 class="fr-h6">{{ step.title }}</h1>
          <p v-if="nextStep" class="fr-text-xs grey--text text--darken-2">
            <b>Étape suivante</b>
            : {{ nextStep.title }}
          </p>
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
    stepTotal() {
      return this.steps.length
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
    saveAndQuit() {
      return this.saveDiagnostic().then(() => {
        this.$router.push(this.quitLink)
      })
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
.v-btn--plain .v-btn__content {
  opacity: 1 !important;
}
</style>
