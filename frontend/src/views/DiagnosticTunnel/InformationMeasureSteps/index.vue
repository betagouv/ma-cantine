<template>
  <div v-if="stepUrlSlug === 'information-convives'" class="py-4">
    <fieldset>
      <legend class="text-left my-3">
        J’informe mes convives sur la part de produits de qualité et durables entrant dans la composition des repas
        servis, et sur les démarches d’acquisition de produits issus d’un PAT (projet alimentaire territorial)
      </legend>
      <v-radio-group class="my-0" v-model="payload.communicatesOnFoodQuality" hide-details @change="updatePayload">
        <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
      </v-radio-group>
    </fieldset>
    <fieldset class="mt-8" :disabled="!payload.communicatesOnFoodQuality">
      <legend class="text-left">Je fais cette information</legend>
      <p class="fr-text-xs mt-1 mb-3">Optionnel</p>
      <v-radio-group class="my-0" v-model="payload.communicationFrequency" hide-details>
        <v-radio
          v-for="item in communicationFrequencies"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :disabled="!payload.communicatesOnFoodQuality"
          :readonly="!payload.communicatesOnFoodQuality"
        ></v-radio>
      </v-radio-group>
    </fieldset>
  </div>
  <div v-else-if="stepUrlSlug === 'mode-information'">
    <fieldset>
      <legend>J’informe les convives sur la qualité des approvisionnements :</legend>
      <p class="fr-text-xs mt-1 mb-3">Plusieurs choix possibles</p>
      <v-checkbox
        hide-details="auto"
        class="ml-8 mb-3 mt-0"
        v-model="payload.communicationSupports"
        :multiple="true"
        v-for="support in communicationSupports"
        :key="support.value"
        :value="support.value"
        :label="support.label"
      />
      <v-row align="center" class="ml-8 mb-3 mt-6 mr-2">
        <v-checkbox v-model="otherSupportEnabled" hide-details class="shrink mt-0"></v-checkbox>
        <v-text-field
          class="my-0 py-0"
          hide-details
          :disabled="!otherSupportEnabled"
          v-model="payload.otherCommunicationSupport"
          label="Autre : donnez plus d'informations"
        ></v-text-field>
      </v-row>
    </fieldset>
  </div>
  <div v-else-if="stepUrlSlug === 'qualite-nutritionnelle'">
    <fieldset>
      <legend class="text-left my-3">J’informe les convives sur la qualité nutritionnelle des repas</legend>
      <v-radio-group class="my-0" v-model="payload.communicatesOnFoodPlan" hide-details @change="updatePayload">
        <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
      </v-radio-group>
    </fieldset>
  </div>
  <div v-else-if="stepUrlSlug === 'lien-communication'">
    <fieldset>
      <legend class="text-left">Lien vers le support de communication</legend>
      <p class="fr-text-xs mt-1 mb-3">Optionnel</p>
      <DsfrTextField
        :rules="[validators.urlOrEmpty]"
        v-model="payload.communicationSupportUrl"
        placeholder="https://"
        validate-on-blur
        class="mt-2"
        style="max-width: 384px;"
      />
    </fieldset>
  </div>
  <component v-else :is="step.componentName" :canteen="canteen" :diagnostic="payload" />
</template>

<script>
import validators from "@/validators"
import InformationMeasureSummary from "@/components/DiagnosticSummary/InformationMeasureSummary"
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"

export default {
  name: "InformationMeasureSteps",
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
  components: { InformationMeasureSummary, DsfrTextField },
  data() {
    const payload = {
      communicatesOnFoodQuality: this.diagnostic.communicatesOnFoodQuality,
      communicationFrequency: this.diagnostic.communicationFrequency,
      communicationSupports: this.diagnostic.communicationSupports,
      otherCommunicationSupport: this.diagnostic.otherCommunicationSupport,
      communicatesOnFoodPlan: this.diagnostic.communicatesOnFoodPlan,
    }
    return {
      communicationFrequencies: Constants.CommunicationFrequencies,
      communicationSupports: Constants.CommunicationSupports,
      otherSupportEnabled: !!payload.otherCommunicationSupport,
      steps: [
        {
          title: "Démarche d’information des convives",
          urlSlug: "information-convives",
        },
        {
          title: "Mode d’information des convives",
          urlSlug: "mode-information",
        },
        {
          title: "Information sur la qualité nutritionnelle",
          urlSlug: "qualite-nutritionnelle",
        },
        {
          title: "Lien vers le support de communication",
          urlSlug: "lien-communication",
        },
        {
          title: "Synthèse",
          isSynthesis: true,
          componentName: "InformationMeasureSummary",
          urlSlug: "synthèse",
        },
      ],
      boolOptions: [
        {
          label: "Oui",
          value: true,
        },
        {
          label: "Non",
          value: false,
        },
      ],
      payload,
    }
  },
  computed: {
    step() {
      const step = this.stepUrlSlug && this.steps.find((step) => step.urlSlug === this.stepUrlSlug)
      return step || this.steps[0]
    },
    validators() {
      return validators
    },
  },
  methods: {
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload, formIsValid: true })
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
    this.updatePayload()
  },
  watch: {
    otherSupportEnabled(val) {
      if (!val) {
        this.payload.otherCommunicationSupport = null
      }
    },
  },
}
</script>

<style scoped>
fieldset:disabled {
  color: rgba(0, 0, 0, 0.38);
}
</style>
