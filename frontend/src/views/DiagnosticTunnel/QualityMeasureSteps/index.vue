<template>
  <v-form v-model="formIsValid" @submit.prevent>
    <div v-if="payload">
      <div v-if="stepUrlSlug === 'mode-de-saisie'">
        <v-radio-group class="my-0" v-model="payload.diagnosticType" hide-details>
          <template v-slot:label>
            <span class="fr-text grey--text text--darken-4">
              Selon le niveau d’information disponible, vous pouvez choisir entre les deux types de saisie suivantes.
            </span>
          </template>
          <v-radio v-for="type in diagnosticTypes" :key="type.key" :label="type.label" :value="type.key">
            <template v-slot:label>
              <span class="grey--text text--darken-3 font-weight-bold">{{ type.label }}</span>
              <span class="fr-text-sm ml-3">{{ type.help }}</span>
            </template>
          </v-radio>
        </v-radio-group>
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
        v-on:tunnel-autofill="onTunnelAutofill"
      />
    </div>
  </v-form>
</template>

<script>
import QualityTotalStep from "./QualityTotalStep"
import BioSiqoStep from "./BioSiqoStep"
import OtherEgalimStep from "./OtherEgalimStep"
import MeatPoultryStep from "./MeatPoultryStep"
import FishStep from "./FishStep"
import MeatFishStep from "./MeatFishStep"
import FamilyFieldsStep from "./FamilyFieldsStep"
import FranceStep from "./FranceStep"
import Constants from "@/constants"
import { getObjectDiff } from "@/utils"

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
    MeatFishStep,
    FamilyFieldsStep,
    FranceStep,
  },
  data() {
    return {
      formIsValid: true,
      purchasesSummary: null,
      diagnosticTypes: Constants.DiagnosticTypes,
      originalValues: null,
      payload: null,
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
        urlSlug: "complet",
      }
      const simplifiedSteps = [
        {
          title: "Valeurs totales des achats Bio et SIQO (Label Rouge, AOC / AOP, IGP, STG)",
          componentName: "BioSiqoStep",
          urlSlug: "valeurs-totales-bio-siqo",
        },
        {
          title: "Valeurs totales des autres achats EGalim",
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
        {
          title: "Zoom sur l'origine France",
          componentName: "FranceStep",
          urlSlug: "valeurs-totales-france",
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
          const urlSlug = characteristicId.toLowerCase().replace("_", "-")
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
      return this.payload?.diagnosticType !== "COMPLETE"
    },
  },
  methods: {
    updatePayloadFromComponent(e) {
      this.$set(this, "payload", e.payload)
    },
    updatePayload() {
      const payloadToSend = getObjectDiff(this.originalValues, this.payload)
      this.$emit("update-payload", { payload: payloadToSend, formIsValid: this.formIsValid })
    },
    onTunnelAutofill(e) {
      this.$set(this, "payload", e.payload)
      this.$emit("tunnel-autofill", e)
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
    initialisePayload() {
      const originalValues = {
        valueTotalHt: this.diagnostic.valueTotalHt,
        diagnosticType: this.diagnostic.diagnosticType || "",
        valueBioHt: this.diagnostic.valueBioHt,
        valueBioDontCommerceEquitableHt: this.diagnostic.valueBioDontCommerceEquitableHt,
        valueSustainableHt: this.diagnostic.valueSustainableHt,
        valueEgalimOthersHt: this.diagnostic.valueEgalimOthersHt,
        valueCommerceEquitableHt: this.diagnostic.valueCommerceEquitableHt,
        valueExternalityPerformanceHt: this.diagnostic.valueExternalityPerformanceHt,
        valueMeatPoultryHt: this.diagnostic.valueMeatPoultryHt,
        valueMeatPoultryEgalimHt: this.diagnostic.valueMeatPoultryEgalimHt,
        valueMeatPoultryFranceHt: this.diagnostic.valueMeatPoultryFranceHt,
        valueFishHt: this.diagnostic.valueFishHt,
        valueFishEgalimHt: this.diagnostic.valueFishEgalimHt,
        valueProduitsDeLaMerFrance: this.diagnostic.valueProduitsDeLaMerFrance,
        valueCharcuterieFrance: this.diagnostic.valueCharcuterieFrance,
        valueFruitsEtLegumesFrance: this.diagnostic.valueFruitsEtLegumesFrance,
        valueProduitsLaitiersFrance: this.diagnostic.valueProduitsLaitiersFrance,
        valueBoulangerieFrance: this.diagnostic.valueBoulangerieFrance,
        valueBoissonsFrance: this.diagnostic.valueBoissonsFrance,
        valueAutresFrance: this.diagnostic.valueAutresFrance,
      }
      const tdGroups = Constants.TeledeclarationCharacteristicGroups
      const completeTdFields = tdGroups.egalim.fields
        .concat(tdGroups.nonEgalim.fields)
        .concat(tdGroups.outsideLaw.fields)
      Object.keys(this.diagnostic).forEach((key) => {
        if (completeTdFields.indexOf(key) > -1) {
          originalValues[key] = this.diagnostic[key]
        }
      })
      this.originalValues = originalValues
      this.payload = JSON.parse(JSON.stringify(originalValues))
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
    this.initialisePayload()
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
    $route() {
      this.initialisePayload()
    },
  },
}
</script>
