<template>
  <v-form v-model="formIsValid" @submit.prevent>
    <div v-if="stepUrlSlug === 'mode-de-saisie'">
      <fieldset>
        <legend class="text-left my-3">
          Vous avez indiqué que votre établissement servait moins de 200 couverts par jour. C’est pourquoi selon le
          niveau d’information disponible, vous pouvez choisir entre les deux types de saisie suivantes.
        </legend>
        <v-radio-group class="my-0" v-model="isSimplifiedDiagnostic" hide-details>
          <v-radio v-for="item in modeOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
        </v-radio-group>
      </fieldset>
    </div>
    <div v-else-if="stepUrlSlug === 'valeurs-totales-bio-siqo'">
      TODO bio siqo
    </div>
    <div v-else-if="stepUrlSlug === 'valeurs-totales-autres'">
      TODO bio siqo
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
      :diagnostic="payload"
      v-on:update-payload="updatePayloadFromComponent"
    />
  </v-form>
</template>

<script>
import QualityMeasureSummary from "@/components/DiagnosticSummary/QualityMeasureSummary"
import QualityTotalStep from "./QualityTotalStep"

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
  },
  data() {
    return {
      formIsValid: true,
      isSimplifiedDiagnostic: true,
      modeOptions: [
        {
          label: "Saisie simplifiée",
          value: true,
        },
        {
          label: "Saisie complète",
          value: false,
        },
      ],
      payload: {
        valueTotalHt: this.diagnostic.valueTotalHt,
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
          urlSlug: "valeurs-totales-bio-siqo",
        },
        {
          title: "Valeurs totales des autres achats EGAlim",
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
  },
  methods: {
    updatePayloadFromComponent(e) {
      this.$set(this, "payload", e.payload)
      this.formIsValid = e.formIsValid
      this.updatePayload()
    },
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload, formIsValid: true })
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
  },
  watch: {
    payload() {
      this.updatePayload()
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
