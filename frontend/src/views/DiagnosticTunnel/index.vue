<template>
  <div class="tunnel text-left d-flex flex-column my-n5" ref="container" v-resize="onResize" style="width: 100%">
    <div class="header px-2">
      <v-row class="mx-auto py-xl-2 constrained align-center my-1 my-sm-3">
        <v-col cols="9" class="py-4 d-flex pl-0 ml-n4" v-if="$vuetify.breakpoint.smAndUp">
          <div v-for="tunnel in tunnels" :key="tunnel.id" class="px-4 header-icon">
            <div v-if="tunnel.id === measure.id" class="d-flex align-center my-1">
              <v-icon small color="primary" class="mr-2">{{ measure.mdiIcon }}</v-icon>
              <p class="fr-text-xs text-uppercase mb-0 grey--text text--darken-2 font-weight-bold">
                {{ measure.shortTitle }}
              </p>
            </div>
            <div v-else>
              <v-icon small color="primary lighten-4" :title="tunnel.shortTitle" aria-hidden="false" role="img">
                {{ tunnel.icon }}
              </v-icon>
            </div>
          </div>
        </v-col>
        <v-col class="text-right py-0" v-if="step">
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
        </v-col>
        <v-col v-if="step && !step.isSynthesis" cols="12" class="pt-0 px-0 mb-n8">
          <DsfrStepper :steps="stepperSteps" :currentStepIdx="stepIdx" />
        </v-col>
      </v-row>
    </div>
    <div
      v-if="diagnostic && !isSynthesis"
      class="flex-grow-1 d-flex flex-column"
      style="width: 100%; overflow-y: scroll; overflow-x: hidden; background: #FFF"
      ref="stepWrapper"
    >
      <v-spacer />
      <div class="mx-auto constrained px-4 py-2" style="width: 100%">
        <component
          :is="`${measure.baseComponent}Steps`"
          :canteen="canteen"
          :diagnostic="diagnostic"
          :stepUrlSlug="stepUrlSlug"
          v-on:update-payload="updatePayload"
          v-on:save-diagnostic-and-go-to-page="saveDiagnosticAndGoToPage"
          v-on:tunnel-autofill="onTunnelAutofill"
          v-on:update-steps="updateSteps"
        />
      </div>
      <v-spacer />
    </div>
    <div
      v-else-if="diagnostic"
      ref="synthesisWrapper"
      class="flex-grow-1 d-flex flex-column"
      style="overflow-y: scroll; overflow-x: hidden;"
    >
      <div class="mx-auto constrained d-flex flex-column flex-grow-1" style="width: 100%; background: #FFF;">
        <SummaryWrapper :measure="measure" :canteen="canteen" :diagnostic="diagnostic" />
      </div>
    </div>
    <div class="footer pa-4 pr-14 pr-xl-0 py-xl-8 d-flex mx-auto constrained align-center" style="width: 100%">
      <div v-if="step && step.isSynthesis && nextTunnelTitle && $vuetify.breakpoint.smAndUp" cols="5">
        <p class="fr-text-xs grey--text text--darken-2 mb-0">
          Onglet suivant :
          <b>{{ nextTunnelTitle }}</b>
        </p>
      </div>
      <v-spacer v-if="$vuetify.breakpoint.smAndUp" />
      <div class="d-block d-sm-flex align-center flex-row-reverse">
        <v-btn
          :disabled="!formIsValid && !isSynthesis"
          @click="continueAction"
          color="primary"
          class="ml-0 ml-sm-4 mb-sm-0"
        >
          {{ continueActionText }}
        </v-btn>
        <p v-if="step && step.isSynthesis" class="mb-0"><router-link :to="firstStepLink">Modifier</router-link></p>
        <p v-else class="mb-0">
          <v-btn
            text
            @click="previousAction"
            :disabled="disablePreviousButton"
            :class="disablePreviousButton ? 'fr-text grey--text text-darken-2' : 'fr-text primary--text'"
          >
            Revenir à l'étape précédente
          </v-btn>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"
import DsfrStepper from "@/components/DsfrStepper"
import SummaryWrapper from "./SummaryWrapper"
import QualityMeasureSteps from "./QualityMeasureSteps"
import WasteMeasureSteps from "./WasteMeasureSteps"
import DiversificationMeasureSteps from "./DiversificationMeasureSteps"
import NoPlasticMeasureSteps from "./NoPlasticMeasureSteps"
import InformationMeasureSteps from "./InformationMeasureSteps"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Le bilan n'a pas été sauvegardé."

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
    SummaryWrapper,
    QualityMeasureSteps,
    WasteMeasureSteps,
    DiversificationMeasureSteps,
    NoPlasticMeasureSteps,
    InformationMeasureSteps,
  },
  data() {
    return {
      formIsValid: true,
      canteen: null,
      diagnostic: null,
      payload: {},
      steps: [],
      tunnels: [
        ...keyMeasures.map((km) => ({
          id: km.id,
          title: km.title,
          shortTitle: km.shortTitle,
          icon: km.mdiIcon,
          backendField: km.progressField,
        })),
      ],
      bypassLeaveWarning: false,
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
    isSynthesis() {
      return this.step?.isSynthesis
    },
    continueActionText() {
      const onSynthesisView = this.step?.isSynthesis
      if (onSynthesisView) return "Passer à l'onglet suivant"
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
    declaringApproOnly() {
      return this.canteen?.productionType === "groupe" && this.diagnostic.centralKitchenDiagnosticMode === "APPRO"
    },
    isLastTunnel() {
      return !this.nextTunnel || this.declaringApproOnly
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
      const synthesisUrl = "complet"
      return this.steps.filter((s) => s.urlSlug !== synthesisUrl)
    },
    disablePreviousButton() {
      return !this.previousStep || !this.formIsValid
    },
    hasChanged() {
      for (let key in this.payload) if (this.diagnostic[key] !== this.payload[key]) return true
      return false
    },
  },
  methods: {
    updateSteps(steps) {
      this.steps = steps
    },
    updatePayload({ payload, formIsValid }) {
      this.$set(this, "payload", payload)
      this.formIsValid = formIsValid
    },
    saveDiagnosticAndGoToPage({ payload, nextPage }) {
      this.$set(this, "payload", payload)
      this.saveDiagnostic(nextPage)
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
    saveDiagnostic(nextPage) {
      if (!this.canteen || !this.diagnostic) return Promise.reject()
      this.updateProgress()
      return this.$store
        .dispatch("updateDiagnostic", {
          canteenId: this.canteen.id,
          id: this.diagnostic.id,
          payload: this.payload,
        })
        .then((response) => {
          // if the save is successful, make sure we are showing the up to date data
          Object.assign(this.diagnostic, response)
          this.bypassLeaveWarning = true
          if (nextPage) this.$router.push(nextPage)
        })
        .catch((e) => {
          if (e.jsonPromise) return e.jsonPromise.then(this.showBackendErrorMessage).then(() => Promise.reject())
          this.$store.dispatch("notifyServerError", e)
          return Promise.reject()
        })
    },
    continueAction() {
      if (!this.formIsValid) return
      this.saveDiagnostic()
        .then(() => {
          if (this.nextStep) {
            this.$router.push({ query: { étape: this.nextStep.urlSlug } })
            this.$refs["stepWrapper"].scrollTop = 0
            this.$refs["synthesisWrapper"].scrollTop = 0
          } else if (this.isLastTunnel) {
            this.$router.push({
              name: "MyProgress",
              params: { measure: "etablissement" },
            })
          } else if (this.nextTunnel) {
            this.$router.push({
              name: "MyProgress",
              params: { measure: this.nextTunnel.id },
            })
          } else {
            this.$router.push({
              name: "DashboardManager",
              params: {
                canteenUrlComponent: this.canteenUrlComponent,
              },
              query: {
                year: this.year,
              },
            })
          }
        })
        .catch(() => {}) // Empty handler bc we handle the backend error on saveDiagnostic
    },
    previousAction() {
      if (!this.formIsValid) return
      this.saveDiagnostic()
        .then(() => {
          if (this.previousStep) {
            this.$router.push({ query: { étape: this.previousStep.urlSlug } })
            this.$refs["stepWrapper"].scrollTop = 0
          } else {
            this.$router.push({
              name: "MyProgress",
              params: {
                canteenUrlComponent: this.canteenUrlComponent,
                year: this.year,
                measure: this.measureId,
              },
            })
          }
        })
        .catch(() => {}) // Empty handler bc we handle the backend error on saveDiagnostic
    },
    showBackendErrorMessage(error) {
      try {
        const messages = Object.values(error)
        this.$store.dispatch("notify", {
          title: "Veuillez vérifier les erreurs ci-dessous",
          message: messages.join("\n"),
          status: "error",
        })
      } catch (error) {
        this.$store.dispatch("notifyServerError", error)
      }
    },
    updateProgress() {
      const backendField = this.tunnels.find((t) => t.id === this.measureId)?.backendField
      if (backendField) {
        this.payload[backendField] = this.step?.urlSlug
      }
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
        .then(this.quit)
        .catch(() => {})
    },
    quit() {
      this.$router.push(this.quitLink)
    },
    onTunnelAutofill(e) {
      this.updatePayload({ payload: e.payload, formIsValid: true })
      const synthesisStep = this.steps.find((x) => x.isSynthesis)
      if (this.$matomo) {
        this.$matomo.trackEvent("tunnel-bilan", "autofill", this.measureId)
      }
      return this.saveDiagnostic()
        .then(this.$nextTick)
        .then(() => this.$router.push({ query: { étape: synthesisStep.urlSlug } }))
        .then(() => {
          if (e.message) {
            this.$store.dispatch("notify", e.message)
          }
        })
    },
    stepLink(step) {
      return { query: { étape: step.urlSlug } }
    },
    onResize() {
      const height = window.innerHeight
      if (!this.$refs.container) return
      this.$refs.container.style.height = `${height}px`
    },
    handleUnload(e) {
      if (this.hasChanged && !this.bypassLeaveWarning) {
        e.preventDefault()
        e.returnValue = LEAVE_WARNING
      } else {
        delete e["returnValue"]
        this.bypassLeaveWarning = false
      }
    },
    handleRouteChange(next) {
      if (!this.hasChanged || this.bypassLeaveWarning) {
        next()
        this.payload = {}
        this.bypassLeaveWarning = false
        return
      }
      window.confirm(LEAVE_WARNING) ? next() : next(false)
    },
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
  },
  mounted() {
    this.fetchCanteen().then(() => this.fetchDiagnostic())
    this.onResize()
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  beforeRouteUpdate(to, from, next) {
    this.handleRouteChange(next)
  },
  beforeRouteLeave(to, from, next) {
    this.handleRouteChange(next)
  },
  watch: {
    step(newStep) {
      this.replaceStepInUrlMaybe()
      if (newStep) this.updatePageTitle()
      window.scrollTo(0, 0)
    },
  },
}
</script>

<style>
.constrained {
  max-width: 1200px !important;
}
.tunnel {
  background-color: #f5f5fe;
}
.scroll {
  height: 100%;
  overflow-y: scroll;
  overflow-x: hidden;
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
