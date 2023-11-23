<template>
  <v-form v-model="formIsValid" @submit.prevent>
    <div v-if="stepUrlSlug === 'mode-de-saisie'">
      <fieldset>
        <legend class="text-left my-3">
          Selon le niveau d’information disponible, vous pouvez choisir entre les deux types de saisie suivantes.
        </legend>
        <v-radio-group class="my-0" v-model="payload.diagnosticType" hide-details>
          <v-radio v-for="type in diagnosticTypes" :key="type.key" :label="type.label" :value="type.key">
            <template v-slot:label>
              <span class="grey--text text--darken-3 font-weight-bold">{{ type.label }}</span>
              <span class="fr-text-sm ml-3">{{ type.help }}</span>
            </template>
          </v-radio>
        </v-radio-group>
      </fieldset>
    </div>
    <div v-if="stepUrlSlug === 'detailed-step-1'">
      TODO 'detailed-step-1'
    </div>
    <component
      v-else
      :is="step.componentName"
      :canteen="canteen"
      :diagnostic="diagnostic"
      :payload="payload"
      :purchasesSummary="purchasesSummary"
      v-on:update-payload="updatePayloadFromComponent"
    />
  </v-form>
</template>

<script>
import QualityTotalStep from "./QualityTotalStep"
import BioSiqoStep from "./BioSiqoStep"
import OtherEgalimStep from "./OtherEgalimStep"
import MeatPoultryStep from "./MeatPoultryStep"
import FishStep from "./FishStep"
import Constants from "@/constants"

export default {
  name: "QualityMeasureSteps",
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
    BioSiqoStep,
    OtherEgalimStep,
    MeatPoultryStep,
    FishStep,
  },
  data() {
    return {
      formIsValid: true,
      purchasesSummary: null,
      diagnosticTypes: Constants.DiagnosticTypes,
      payload: {
        valueTotalHt: this.diagnostic.valueTotalHt,
        diagnosticType: this.diagnostic.diagnosticType || "SIMPLE",
        valueBioHt: this.diagnostic.valueBioHt,
        valueSustainableHt: this.diagnostic.valueSustainableHt,
        valueEgalimOthersHt: this.diagnostic.valueEgalimOthersHt,
        valueExternalityPerformanceHt: this.diagnostic.valueExternalityPerformanceHt,
        valueMeatPoultryHt: this.diagnostic.valueMeatPoultryHt,
        valueMeatPoultryEgalimHt: this.diagnostic.valueMeatPoultryEgalimHt,
        valueMeatPoultryFranceHt: this.diagnostic.valueMeatPoultryFranceHt,
        valueFishHt: this.diagnostic.valueFishHt,
        valueFishEgalimHt: this.diagnostic.valueFishEgalimHt,
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
        urlSlug: "complet",
      }
      const simplifiedSteps = [
        {
          title: "Valeurs totales des achats Bio et SIQO (Label Rouge, AOC / AOP, IGP, STG)",
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
          componentName: "MeatPoultryStep",
          urlSlug: "valeurs-totales-viandes-volailles",
        },
        {
          title: "Zoom sur la famille « produits de la mer et de l’aquaculture »",
          componentName: "FishStep",
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
    fetchPurchasesSummary() {
      fetch(`/api/v1/canteenPurchasesSummary/${this.canteen.id}?year=${this.diagnostic.year}`)
        .then((response) => (response.ok ? response.json() : {}))
        .then((response) => {
          if (Object.values(response).some((x) => !!x)) {
            this.$set(this, "purchasesSummary", response)
          } else this.$set(this, "purchasesSummary", null)
        })
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
    this.fetchPurchasesSummary()
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
