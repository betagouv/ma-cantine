<template>
  <v-form v-model="formIsValid" @submit.prevent>
    <div v-if="stepUrlSlug === 'mode-de-saisie'">
      <fieldset>
        <legend class="text-left my-3">
          Vous avez indiqué que votre établissement servait moins de 200 couverts par jour. C’est pourquoi selon le
          niveau d’information disponible, vous pouvez choisir entre les deux types de saisie suivantes.
        </legend>
        <v-radio-group class="my-0" v-model="payload.diagnosticType" hide-details>
          <v-radio v-for="type in diagnosticTypes" :key="type.key" :label="type.label" :value="type.key">
            <template v-slot:label>
              <span class="grey--text text--darken-3 font-weight-bold">{{ type.label }}</span>
              <span class="body-2 ml-3">{{ type.help }}</span>
            </template>
          </v-radio>
        </v-radio-group>
      </fieldset>
    </div>
    <div v-if="stepUrlSlug === 'valeurs-totales-viandes-volailles'">
      TODO valeurs-totales-viandes-volailles
    </div>
    <div v-if="stepUrlSlug === 'valeurs-totales-mer-aquaculture'">
      TODO valeurs-totales-mer-aquaculture
    </div>
    <div v-if="stepUrlSlug === 'detailed-step-1'">
      TODO 'detailed-step-1
    </div>
    <component
      v-else
      :is="step.componentName"
      :canteen="canteen"
      :diagnostic="diagnostic"
      :payload="payload"
      v-on:update-payload="updatePayloadFromComponent"
    />
  </v-form>
</template>

<script>
import QualityMeasureSummary from "@/components/DiagnosticSummary/QualityMeasureSummary"
import QualityTotalStep from "./QualityTotalStep"
import BioSiqoStep from "./BioSiqoStep"
import OtherEgalimStep from "./OtherEgalimStep"
import Constants from "@/constants"

export default {
  name: "QualitySteps",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    stepUrlSlug: {
      type: String,
    },
  },
  components: {
    QualityTotalStep,
    QualityMeasureSummary,
    BioSiqoStep,
    OtherEgalimStep,
  },
  data() {
    return {
      formIsValid: true,
      diagnosticTypes: Constants.DiagnosticTypes,
      payload: {
        valueTotalHt: this.diagnostic.valueTotalHt,
        diagnosticType: this.diagnostic.diagnosticType,
        valueBioHt: this.diagnostic.valueBioHt,
        valueSustainableHt: this.diagnostic.valueSustainableHt,
        valueEgalimOthersHt: this.diagnostic.valueEgalimOthersHt,
        valueExternalityPerformanceHt: this.diagnostic.valueExternalityPerformanceHt,
      },
    }
  },
  computed: {
    step() {
      const step = this.stepUrlSlug && this.steps.find((step) => step.urlSlug === this.stepUrlSlug)
      return step || this.steps[0]
    },
    steps() {
      const firstSteps = [
        {
          title: "Valeurs totales des achats alimentaires",
          componentName: "QualityTotalStep",
          urlSlug: "total",
        },
        {
          title: "Choix du mode de saisie",
          urlSlug: "mode-de-saisie",
        },
      ]
      const lastStep = {
        title: "Synthèse",
        isSynthesis: true,
        componentName: "QualityMeasureSummary",
        urlSlug: "synthèse",
      }
      const simplifiedSteps = [
        {
          title: "Valeurs totales des achats Bio et SIQO (AOP/AOC, IGP, STG, Label Rouge)",
          componentName: "BioSiqoStep",
          urlSlug: "valeurs-totales-bio-siqo",
        },
        {
          title: "Valeurs totales des autres achats EGAlim",
          componentName: "OtherEgalimStep",
          urlSlug: "valeurs-totales-autres",
        },
        {
          title: "Zoom sur la famille « viandes et volailles »",
          urlSlug: "valeurs-totales-viandes-volailles",
        },
        {
          title: "Zoom sur la famille « produits de la mer et de l’aquaculture »",
          urlSlug: "valeurs-totales-mer-aquaculture",
        },
      ]
      const detailedSteps = [
        {
          title: "Detailed step 1",
          urlSlug: "detailed-step-1",
        },
      ]
      const intermediarySteps = this.isSimplifiedDiagnostic ? simplifiedSteps : detailedSteps
      return [...firstSteps, ...intermediarySteps, lastStep]
    },
    isSimplifiedDiagnostic() {
      return this.payload.diagnosticType !== "COMPLETE"
    },
  },
  methods: {
    updatePayloadFromComponent(e) {
      this.$set(this, "payload", e.payload)
    },
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload, formIsValid: this.formIsValid })
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
  },
  watch: {
    payload: {
      handler() {
        this.updatePayload()
      },
      deep: true,
    },
    formIsValid() {
      this.updatePayload()
    },
    isSimplifiedDiagnostic() {
      this.$emit("update-steps", this.steps)
    },
  },
}
</script>
