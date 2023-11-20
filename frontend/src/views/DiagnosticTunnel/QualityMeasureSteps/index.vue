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
    <component
      v-else-if="step.characteristicId"
      :is="step.componentName"
      :diagnostic="diagnostic"
      :payload="payload"
      :purchasesSummary="purchasesSummary"
      :characteristicId="step.characteristicId"
      :groupId="step.groupId"
      v-on:update-payload="updatePayloadFromComponent"
    />
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
import QualityMeasureSummary from "@/components/DiagnosticSummary/QualityMeasureSummary"
import QualityTotalStep from "./QualityTotalStep"
import BioSiqoStep from "./BioSiqoStep"
import OtherEgalimStep from "./OtherEgalimStep"
import MeatPoultryStep from "./MeatPoultryStep"
import FishStep from "./FishStep"
import MeatFishStep from "./MeatFishStep"
import FamilyFieldsStep from "./FamilyFieldsStep"
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
    MeatPoultryStep,
    FishStep,
    MeatFishStep,
    FamilyFieldsStep,
  },
  data() {
    const payload = { diagnosticType: this.diagnostic.diagnosticType }
    Object.keys(this.diagnostic).forEach((key) => {
      if (key.startsWith("value")) {
        payload[key] = this.diagnostic[key]
      }
    })
    return {
      formIsValid: true,
      purchasesSummary: null,
      diagnosticTypes: Constants.DiagnosticTypes,
      payload,
      characteristics: Constants.TeledeclarationCharacteristics,
      characteristicGroups: Constants.TeledeclarationCharacteristicGroups,
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
          componentName: "MeatPoultryStep",
          urlSlug: "valeurs-totales-viandes-volailles",
        },
        {
          title: "Zoom sur la famille « produits de la mer et de l’aquaculture »",
          componentName: FishStep,
          urlSlug: "valeurs-totales-mer-aquaculture",
        },
      ]
      const detailedSteps = [
        {
          title: "Valeurs totales par famille de produit",
          componentName: MeatFishStep,
          urlSlug: "valeurs-totales-viandes-aquaculture",
        },
      ]
      for (const groupId in this.characteristicGroups) {
        // egalim, nonEgalim, outsideLaw
        const groupCharacteristics = this.characteristicGroups[groupId].characteristics
        for (const characteristicIdx in groupCharacteristics) {
          const characteristicId = groupCharacteristics[characteristicIdx]
          const characteristic = this.characteristics[characteristicId]
          const urlSlug = characteristicId.toLowerCase() // TODO: replace underscores with hyphens
          detailedSteps.push({
            title: `Valeurs totales par famille de produit des achats « ${characteristic.text} »`,
            componentName: FamilyFieldsStep,
            characteristicId: characteristicId,
            groupId: groupId,
            urlSlug,
          })
        }
      }
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
          const hasSummary = Object.values(response).some((x) => !!x)
          if (hasSummary) this.$set(this, "purchasesSummary", response)
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
