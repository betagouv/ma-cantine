<template>
  <div class="text-left">
    <v-row class="header">
      <v-row class="mx-auto constrained align-center pt-6">
        <v-col cols="9">
          <v-row>
            <div v-for="tunnel in tunnels" :key="tunnel.id" class="px-4 header-icon">
              <div v-if="tunnel.id === measure.id" class="d-flex align-center my-1">
                <v-icon small color="primary" class="mr-2">{{ measure.mdiIcon }}</v-icon>
                <p class="fr-text-xs text-uppercase mb-0 grey--text text--darken-2 font-weight-bold">
                  {{ measure.shortTitle }}
                </p>
              </div>
              <div v-else>
                <v-icon small color="primary lighten-4">{{ tunnel.icon }}</v-icon>
              </div>
            </div>
          </v-row>
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
          <DsfrStepper :steps="stepperSteps" :currentStepIdx="stepIdx" />
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
      <v-row class="mx-auto constrained align-center">
        <v-col v-if="step && step.isSynthesis && nextTunnelTitle" cols="5">
          <p class="fr-text-xs grey--text text--darken-2 mb-0">
            Onglet suivant :
            <b>{{ nextTunnelTitle }}</b>
          </p>
        </v-col>
        <v-spacer />
        <v-col>
          <v-row class="py-10 px-4 align-center flex-row-reverse">
            <v-btn :disabled="!formIsValid" @click="continueAction" color="primary" class="ml-4">
              {{ continueActionText }}
            </v-btn>
            <p v-if="step && step.isSynthesis" class="mb-0"><router-link :to="firstStepLink">Modifier</router-link></p>
            <p v-else class="mb-0">
              <router-link v-if="previousStep && formIsValid" :to="stepLink(previousStep)">
                Revenir à l'étape précédente
              </router-link>
              <a v-else class="grey--text text-darken-2" role="link" aria-disabled="true">
                Revenir à l'étape précédente
              </a>
            </p>
          </v-row>
        </v-col>
      </v-row>
    </v-row>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"
import DsfrStepper from "@/components/DsfrStepper"
import QualityMeasureSteps from "./QualityMeasureSteps"
import WasteMeasureSteps from "./WasteMeasureSteps"
import DiversificationMeasureSteps from "./DiversificationMeasureSteps"
import NoPlasticMeasureSteps from "./NoPlasticMeasureSteps"
import InformationMeasureSteps from "./InformationMeasureSteps"

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
  components: {
    DsfrStepper,
    QualityMeasureSteps,
    WasteMeasureSteps,
    DiversificationMeasureSteps,
    NoPlasticMeasureSteps,
    InformationMeasureSteps,
  },
  data() {
    return {
      formIsValid: false,
      canteen: null,
      diagnostic: null,
      payload: {},
      steps: [],
      tunnels: [
        ...keyMeasures.map((km) => ({ id: km.id, title: km.title, shortTitle: km.shortTitle, icon: km.mdiIcon })),
      ],
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
      const returnToTable = !this.nextTunnel
      if (returnToTable) return "Retour au tableau de bord"
      const nextIsNewMeasure = this.step?.isSynthesis
      if (nextIsNewMeasure) return "Passer à l'onglet suivant"
      const nextIsSynthesis = this.nextStep?.isSynthesis
      if (nextIsSynthesis) return "Voir la synthèse"
      return "Sauvegarder et continuer"
    },
    nextTunnel() {
      const currentTunnelIdx = this.tunnels.findIndex((t) => t.id === this.measureId)
      if (currentTunnelIdx <= this.tunnels.length) {
        return this.tunnels[currentTunnelIdx + 1]
      }
      return null
    },
    nextTunnelTitle() {
      return this.nextTunnel?.shortTitle
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
      return this.stepLink(this.steps[0])
    },
    stepperSteps() {
      // we do not count the synthèse as a step, this assumes that all steps will include a final synthèse
      const synthesisUrl = "synthèse"
      return this.steps.filter((s) => s.urlSlug !== synthesisUrl)
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
        } else if (this.nextTunnel) {
          this.$router.push({ params: { measureId: this.nextTunnel.id }, query: {} })
        } else {
          this.$router.push({
            name: "DashboardManager",
            params: {
              canteenUrlComponent: this.canteenUrlComponent,
            },
          })
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
      return this.saveDiagnostic()
        .then(() => {
          this.$router.push(this.quitLink)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    stepLink(step) {
      return { query: { étape: step.urlSlug } }
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
a[aria-disabled="true"] {
  cursor: not-allowed;
}
.header-icon {
  border-right: #e5e5e5 solid 1px;
}
</style>
