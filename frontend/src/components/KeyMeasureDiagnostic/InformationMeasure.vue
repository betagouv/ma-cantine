<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodQuality"
      label="J’informe mes convives sur la part de produits de qualité et durables, entrant dans la composition des repas servis, et sur les démarches d’acquisition de produits issus d'un PAT (projet alimentaire territorial)"
      :readonly="readonly"
      :disabled="readonly"
    />

    <DsfrRadio
      label="Je fais cette information :"
      v-model="diagnostic.communicationFrequency"
      hide-details
      :items="communicationFrequencies"
      :readonly="readonly"
      :disabled="readonly"
      optionClasses="ml-8"
      class="mt-3"
    />

    <fieldset class="mt-3 mb-4">
      <legend class="text-left my-3">J'informe sur la qualité des approvisionnements :</legend>
      <v-checkbox
        hide-details="auto"
        class="ml-8 mb-3 mt-0"
        v-model="diagnostic.communicationSupports"
        :multiple="true"
        v-for="support in communicationSupports"
        :key="support.value"
        :value="support.value"
        :label="support.label"
        :readonly="readonly"
        :disabled="readonly"
      />
      <v-row align="center" class="ml-8 mb-3 mt-0 mr-2">
        <v-checkbox
          v-model="otherSupportEnabled"
          hide-details
          class="shrink mt-0"
          :readonly="readonly"
          :disabled="readonly"
          aria-label="Autre : donnez plus d'informations"
        ></v-checkbox>
        <!-- Will leave this UI version of the text-field since it is next to a checkbox -->
        <v-text-field
          class="my-0 py-0 other-text-input"
          hide-details
          :disabled="!otherSupportEnabled || readonly"
          v-model="diagnostic.otherCommunicationSupport"
          label="Autre : donnez plus d'informations"
          :readonly="readonly"
        ></v-text-field>
      </v-row>
    </fieldset>

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodPlan"
      label="J'informe sur la qualité nutritionnelle des repas"
      :readonly="readonly"
      :disabled="readonly"
      class="mb-6"
    />

    <DsfrTextField
      :rules="[validators.urlOrEmpty]"
      v-model="diagnostic.communicationSupportUrl"
      placeholder="https://"
      validate-on-blur
      :readonly="readonly"
      :disabled="readonly"
      class="mt-2"
      label="Lien vers le support de communication"
    />
  </div>
</template>

<script>
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrRadio from "@/components/DsfrRadio"
import Constants from "@/constants"

export default {
  components: { DsfrTextField, DsfrRadio },
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      communicationFrequencies: Constants.CommunicationFrequencies,
      communicationSupports: Constants.CommunicationSupports,
      otherSupportEnabled: !!this.diagnostic.otherCommunicationSupport,
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
  watch: {
    otherSupportEnabled(val) {
      if (!val) {
        this.diagnostic.otherCommunicationSupport = null
      }
    },
  },
}
</script>
