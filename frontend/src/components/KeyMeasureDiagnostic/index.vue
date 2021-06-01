<template>
  <div>
    <h2 id="modal-title" class="mb-3" tabindex="-1"><KeyMeasureTitle :measure="measure" /></h2>

    <v-form ref="form" v-model="formIsValid" @submit.prevent>
      <QualityMeasureDiagnostic
        v-if="measureDiagnosticComponentName === 'QualityMeasureDiagnostic'"
        :diagnostics="diagnosticsCopy"
      />
      <component v-else :is="measureDiagnosticComponentName" :diagnostic="diagnosticsCopy.latest" />
      <v-row class="mt-2 pa-4">
        <v-spacer></v-spacer>
        <v-btn x-large color="primary" @click="saveDiagnostic">Valider</v-btn>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import KeyMeasureTitle from "@/components/KeyMeasureTitle"
import DiversificationMeasureDiagnostic from "@/components/KeyMeasureDiagnostic/DiversificationMeasure"
import InformationMeasureDiagnostic from "@/components/KeyMeasureDiagnostic/InformationMeasure"
import NoPlasticMeasureDiagnostic from "@/components/KeyMeasureDiagnostic/NoPlasticMeasure"
import QualityMeasureDiagnostic from "@/components/KeyMeasureDiagnostic/QualityMeasure"
import WasteMeasureDiagnostic from "@/components/KeyMeasureDiagnostic/WasteMeasure"
import { saveDiagnostics } from "@/data/KeyMeasures.js"

export default {
  components: {
    KeyMeasureTitle,
    DiversificationMeasureDiagnostic,
    InformationMeasureDiagnostic,
    NoPlasticMeasureDiagnostic,
    QualityMeasureDiagnostic,
    WasteMeasureDiagnostic,
  },
  props: ["measure", "afterSave", "diagnosticsCopy"],
  data() {
    return {
      formIsValid: true,
    }
  },
  methods: {
    saveDiagnostic() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        window.alert("Merci de vérifier les champs en rouge et réessayer")
        return
      }
      if (this.isAuthenticated) {
        this.saveInServer().then(() => this.$emit("afterSave"))
      } else {
        this.saveInLocalStorage()
        this.$emit("afterSave")
      }
    },
    saveInServer() {
      return Promise.all([
        this.$store.dispatch("updateDiagnosis", {
          canteenId: this.userCanteen.id,
          id: this.diagnosticsCopy.latest.id,
          payload: this.diagnosticsCopy.latest,
        }),
        this.$store.dispatch("updateDiagnosis", {
          canteenId: this.userCanteen.id,
          id: this.diagnosticsCopy.previous.id,
          payload: this.diagnosticsCopy.previous,
        }),
      ])
    },
    saveInLocalStorage() {
      this.$store.dispatch("saveLocalStorageDiagnosis", this.diagnosticsCopy.latest)
      this.$store.dispatch("saveLocalStorageDiagnosis", this.diagnosticsCopy.previous)
    },
    async submit() {
      await saveDiagnostics(this.diagnostics)
      this.$emit("afterSave")
    },
  },
  computed: {
    measureDiagnosticComponentName() {
      return this.measure ? this.measure.baseComponent + "Diagnostic" : null
    },
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
    userCanteen() {
      return this.$store.state.userCanteens.length > 0 ? this.$store.state.userCanteens[0] : null
    },
  },
}
</script>

<style scoped lang="scss">
#diagnostic-form {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  min-height: 500px;

  #submit {
    color: $ma-cantine-white;
    font-size: 24px;
    background-color: $ma-cantine-orange;
    width: 10em;
    padding: 0.2em;
    border-radius: 1em;
    cursor: pointer;
    margin-left: auto;
    text-align: center;
    border: none;
    margin-top: 10px;
    margin-bottom: 10px;
  }
}
</style>
