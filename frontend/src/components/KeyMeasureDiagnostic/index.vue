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
        this.$store.dispatch("notifyRequiredFieldsError")
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
      const saveOperations = []

      for (let i = 0; i < Object.values(this.diagnosticsCopy).length; i++) {
        const diagnostic = Object.values(this.diagnosticsCopy)[i]

        if (diagnostic.id) {
          saveOperations.push(
            this.$store.dispatch("updateDiagnostic", {
              canteenId: this.userCanteen.id,
              id: diagnostic.id,
              payload: diagnostic,
            })
          )
        } else {
          saveOperations.push(
            this.$store.dispatch("createDiagnostic", {
              canteenId: this.userCanteen.id,
              payload: diagnostic,
            })
          )
        }
      }

      return Promise.all([saveOperations])
    },
    saveInLocalStorage() {
      this.$store.dispatch("saveLocalStorageDiagnostic", this.diagnosticsCopy.latest)
      this.$store.dispatch("saveLocalStorageDiagnostic", this.diagnosticsCopy.previous)
      this.$store.dispatch("saveLocalStorageDiagnostic", this.diagnosticsCopy.provisionalYear1)
      this.$store.dispatch("saveLocalStorageDiagnostic", this.diagnosticsCopy.provisionalYear2)
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
