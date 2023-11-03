<template>
  <div v-if="step" class="text-left">
    <v-row class="header">
      <v-row class="mx-auto constrained pt-6">
        <v-col cols="9">
          <!-- TODO: section icons -->
          <p class="fr-text-xs text-transform-uppercase mb-0">{{ measure.title }}</p>
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
        <v-col v-if="!step.isSynthesis" cols="12">
          <p class="fr-text-sm">Étape {{ stepIdx + 1 }} sur {{ measure.stepTotal }}</p>
          <h1 class="fr-h6">{{ step.title }}</h1>
          <!-- TODO: DSFR stepper component which will include everything else in this column as well -->
          <p v-if="nextStep" class="fr-text-xs grey--text text--darken-2">
            <b>Étape suivante</b>
            : {{ nextStep.title }}
          </p>
        </v-col>
      </v-row>
    </v-row>
    <div v-if="diagnostic" class="mx-auto constrained pa-10">
      <!-- TODO: padding/centering and sorting out scrolling -->
      <!-- TODO: question OR synthesis (move existing syntheses to /components/ to reuse) -->
      <!-- TODO: make 6 components for each measure which then handles the question stepping -->
      <component :is="step.componentName" :canteen="canteen" :diagnostic="diagnostic" @updatePayload="updatePayload" />
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
            <p v-if="step.isSynthesis" class="mb-0"><router-link :to="firstStep">Modifier</router-link></p>
            <p v-else class="mb-0">
              <!-- TODO: handle previousStep === null properly -->
              <router-link :to="previousStep ? previousStep.to : {}">
                Revenir à l'étape précédente
              </router-link>
            </p>
            <!-- TODO: make this tab first instead of Revenir link -->
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
import QualityTotalStep from "./quality/QualityTotalStep"
import QualityMeasureSummary from "@/components/DiagnosticSummary/QualityMeasureSummary"

const stepsByMeasure = {
  "qualite-des-produits": [
    {
      title: "Valeurs totales des achats alimentaires",
      componentName: "QualityTotalStep",
      urlSlug: "total",
    },
    {
      title: "Synthèse",
      isSynthesis: true,
      componentName: "QualityMeasureSummary",
      urlSlug: "synthèse",
    },
  ],
}

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
  components: { QualityTotalStep, QualityMeasureSummary },
  data() {
    return {
      formIsValid: false,
      canteen: null,
      diagnostic: null,
      payload: {},
      steps: stepsByMeasure[this.measureId],
    }
  },
  computed: {
    canteenId() {
      return this.canteenUrlComponent.split("--")[0]
    },
    measure() {
      return {
        title: "Qualité des approvisionnements",
        stepTotal: 6,
        id: "qualite-des-produits",
      }
    },
    stepUrlSlug() {
      return this.$route.query.étape
    },
    stepIdx() {
      let idx = 0
      if (this.stepUrlSlug) {
        idx = this.steps.findIndex((step) => step.urlSlug === this.stepUrlSlug)
        idx = idx > -1 ? idx : 0
        // TODO: remove query param from URL with a router.replace if it's nonsense ?
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
      const returnToTable = this.step.isFinal
      if (returnToTable) return "Retour au tableau de bord"
      const nextIsNewMeasure = this.step.isSynthesis
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
    firstStep() {
      return { params: { componentName: this.steps[0].componentName } }
    },
  },
  methods: {
    updatePayload({ payload, formIsValid }) {
      this.payload = payload
      this.formIsValid = formIsValid
    },
    fetchCanteen() {
      const id = this.canteenId
      return this.$store.dispatch("fetchCanteen", { id }).then((canteen) => {
        this.$set(this, "canteen", canteen)
      })
      // TODO: error handling
    },
    fetchDiagnostic() {
      if (!this.canteen) return
      // TODO: error handling for no diagnostic found
      this.diagnostic = this.canteen.diagnostics.find((d) => d.year === +this.year)
    },
    validateForm() {
      this.formIsValid = true
    },
    saveDiagnostic() {
      if (!this.canteen || !this.diagnostic) return Promise.reject()
      this.updateProgress()
      return this.$store.dispatch("updateDiagnostic", {
        canteenId: this.canteen.id,
        id: this.diagnostic.id,
        payload: this.payload,
      })
      // TODO: error handling
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
      // TODO: is any error going to fail too silently?
    },
    setPageTitle() {
      document.title = `${this.step?.title} - ${this.year} - ${this.canteen?.name} - ${this.$store.state.pageTitleSuffix}`
    },
  },
  mounted() {
    this.fetchCanteen().then(() => this.fetchDiagnostic())
    this.setPageTitle()
  },
  $watch: {
    step() {
      this.setPageTitle()
    },
  },
}
</script>

<style>
.header {
  background-color: #f5f5fe;
  /* TODO: sticky */
  /* position: fixed;
  top: 0%; */
}
.footer {
  background-color: #f5f5fe;
  /* TODO: sticky */
  /* position: fixed;
  bottom: 0%; */
}
</style>
