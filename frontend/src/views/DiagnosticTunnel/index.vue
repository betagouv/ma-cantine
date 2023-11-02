<template>
  <div class="text-left">
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
          <p class="fr-text-sm">Étape {{ step.number }} sur {{ measure.stepTotal }}</p>
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
      <component :is="step.componentName" :diagnostic="diagnostic" @updatePayload="updatePayload" />
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
            <p v-if="step.isSynthesis" class="mb-0"><router-link :to="measure.firstStep">Modifier</router-link></p>
            <p v-else class="mb-0">
              <!-- TODO: handle previousStep === null properly -->
              <router-link :to="previousStep ? previousStep.to : {}">
                Revenir à l'étape précédente
              </router-link>
            </p>
            <v-btn primary :disabled="!formIsValid" @click="continueAction" class="ml-4">
              {{ continueActionText }}
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-row>
  </div>
</template>

<script>
import QualityTotal from "./quality/QualityTotal"

export default {
  name: "DiagnosticTunnel",
  components: { QualityTotal },
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
    // TODO: have optional componentName in link to go directly to a particular step
  },
  data() {
    return {
      formIsValid: false,
      canteen: null,
      diagnostic: null,
      payload: {},
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
        firstStep: {}, // TODO: this should be in the structure of a router-link `to`
      }
    },
    step() {
      // TODO: find from list using prop `componentName`, default to first step in measure
      return {
        title: "Valeurs totales des achats alimentaires",
        number: 1,
        next: {
          title: "Synthèse",
          isSynthesis: true,
        },
        previous: null,
        componentName: "QualityTotal",
      }
    },
    nextStep() {
      return this.step.next
    },
    previousStep() {
      return this.step.previous
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
  },
  methods: {
    updatePayload(payload) {
      this.payload = payload
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
      if (!this.canteen || !this.diagnostic) return
      this.updateProgress()
      this.$store.dispatch("updateDiagnostic", {
        canteenId: this.canteen.id,
        id: this.diagnostic.id,
        payload: this.payload,
      })
      // TODO: error handling
    },
    continueAction() {
      if (!this.formIsValid) return
      this.saveDiagnostic().then(() => {
        this.$route.push(this.nextStep.to)
      })
    },
    updateProgress() {
      if (this.isSynthesis) this.payload.qualityProgress = "COMPLETE"
      else if (this.step.isFinal) this.payload.isComplete = true
      this.payload.qualityProgress = this.nextStep?.componentName
      // TODO: is any error going to fail too silently?
    },
  },
  mounted() {
    this.fetchCanteen().then(() => this.fetchDiagnostic())
    // TODO: document.title
  },
}
</script>

<style>
.header {
  background-color: #f5f5fe;
  /* position: fixed;
  top: 0%; */
}
.footer {
  background-color: #f5f5fe;
  /* position: fixed;
  bottom: 0%; */
}
</style>
