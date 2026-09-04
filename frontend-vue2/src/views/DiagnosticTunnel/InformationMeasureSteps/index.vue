<template>
  <v-form @submit.prevent v-model="formIsValid">
    <div v-if="stepUrlSlug === 'information-convives'">
      <LastYearAutofillOption
        :canteen="canteen"
        :diagnostic="diagnostic"
        :fields="fields"
        @tunnel-autofill="onTunnelAutofill"
        class="mb-xs-6 mb-xl-16"
      />
      <DsfrRadio
        label="J’informe mes convives sur la part de produits de qualité et durables entrant dans la composition des repas
          servis, et sur les démarches d’acquisition de produits issus d’un PAT (projet alimentaire territorial)"
        v-model="payload.communicatesOnFoodQuality"
        hide-details
        optional
        yesNo
      />
      <DsfrRadio
        label="Je fais cette information"
        v-model="payload.communicationFrequency"
        hide-details
        optional
        :items="communicationFrequencies"
        :disabled="!payload.communicatesOnFoodQuality"
        :readonly="!payload.communicatesOnFoodQuality"
        class="mt-8"
      />
    </div>
    <div v-else-if="stepUrlSlug === 'mode-information'">
      <fieldset>
        <legend>
          J’informe les convives sur la qualité des approvisionnements :
          <span class="fr-hint-text my-2">Optionnel</span>
        </legend>
        <v-checkbox
          hide-details="auto"
          class="mb-3 mt-0"
          v-model="payload.communicationSupports"
          :multiple="true"
          v-for="support in communicationSupports"
          :key="support.value"
          :value="support.value"
          :label="support.label"
        />
        <v-row class="ml-0 mb-3 mt-0 mr-2">
          <v-checkbox
            v-model="otherSupportEnabled"
            hide-details
            class="mt-0"
            aria-label="Autre : donnez plus d'informations"
          ></v-checkbox>
          <v-text-field
            class="my-0 py-0 other-text-input"
            hide-details
            ref="other-support-field"
            :disabled="!otherSupportEnabled"
            v-model="payload.otherCommunicationSupport"
            label="Autre : donnez plus d'informations"
            :rules="otherSupportEnabled ? [validators.required] : []"
          ></v-text-field>
        </v-row>
      </fieldset>
    </div>
    <DsfrRadio
      v-else-if="stepUrlSlug === 'qualite-nutritionnelle'"
      label="J’informe les convives sur la qualité nutritionnelle des repas"
      v-model="payload.communicatesOnFoodPlan"
      hide-details
      optional
      yesNo
    />
    <div v-else-if="stepUrlSlug === 'lien-communication'">
      <DsfrTextField
        label="Lien vers le support de communication"
        :rules="[validators.urlOrEmpty]"
        v-model="payload.communicationSupportUrl"
        placeholder="https://"
        validate-on-blur
      />
    </div>
  </v-form>
</template>

<script>
import LastYearAutofillOption from "../LastYearAutofillOption"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrRadio from "@/components/DsfrRadio"
import validators from "@/validators"
import Constants from "@/constants"

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
  components: { LastYearAutofillOption, DsfrTextField, DsfrRadio },
  data() {
    return {
      formIsValid: true,
      communicationFrequencies: Constants.CommunicationFrequencies,
      communicationSupports: Constants.CommunicationSupports,
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
          urlSlug: "complet",
        },
      ],
      payload: {},
      fields: [
        "communicatesOnFoodQuality",
        "communicationFrequency",
        "communicationSupports",
        "otherCommunicationSupport",
        "communicatesOnFoodPlan",
        "communicationSupportUrl",
      ],
      otherSupportEnabled: undefined,
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
      this.$emit("update-payload", { payload: this.payload, formIsValid: this.formIsValid })
    },
    initialisePayload() {
      const payload = {}
      this.fields.forEach((f) => (payload[f] = this.diagnostic[f]))
      this.otherSupportEnabled = !!this.payload.otherCommunicationSupport
      this.$set(this, "payload", payload)
    },
    onTunnelAutofill(e) {
      this.$set(this, "payload", e.payload)
      this.$emit("tunnel-autofill", e)
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
    this.initialisePayload()
    this.updatePayload()
  },
  watch: {
    otherSupportEnabled(val) {
      if (val) this.$nextTick().then(this.$refs["other-support-field"]?.validate)
      else this.payload.otherCommunicationSupport = null
    },
    payload: {
      handler() {
        this.updatePayload()
      },
      deep: true,
    },
    formIsValid() {
      this.updatePayload()
    },
    $route() {
      this.initialisePayload()
    },
  },
}
</script>

<style scoped>
fieldset:disabled {
  color: rgba(0, 0, 0, 0.38);
}
</style>
