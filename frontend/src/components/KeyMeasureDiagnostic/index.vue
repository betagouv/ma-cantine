<template>
  <div>
    <h2 id="modal-title" class="mb-3" tabindex="-1"><KeyMeasureTitle :measure="measure" /></h2>

    <v-form ref="form" v-model="formIsValid" @submit.prevent>
      <QualityMeasureDiagnostic
        v-if="measureDiagnosticComponentName === 'QualityMeasureDiagnostic'"
        :diagnostics="diagnosticsCopy"
        :canteen="canteen"
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
  props: ["measure", "afterSave", "diagnosticsCopy", "canteen"],
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
      this.saveInLocalStorage()
      this.$emit("afterSave")
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
