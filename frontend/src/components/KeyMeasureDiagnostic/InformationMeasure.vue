<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodQuality"
      label="J’informe mes convives sur la part de produits de qualité et durables, entrant dans la composition des repas servis, et sur les démarches d’acquisition de produits issus d'un PAT (projet alimentaire territorial)"
      :readonly="readonly"
      :disabled="readonly"
    />

    <fieldset class="mt-3 mb-4">
      <legend class="text-left my-3">Je fais cette information :</legend>
      <v-radio-group class="my-0" v-model="diagnostic.communicationFrequency" hide-details>
        <v-radio
          class="ml-8"
          v-for="item in communicationFrequencies"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :readonly="readonly"
          :disabled="readonly"
        ></v-radio>
      </v-radio-group>
    </fieldset>

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
        ></v-checkbox>
        <v-text-field
          class="my-0 py-0"
          hide-details
          :disabled="!otherSupportEnabled || readonly"
          v-model="diagnostic.otherCommunicationSupport"
          label="Autre : donnez plus d'informations"
          :readonly="readonly"
        ></v-text-field>
      </v-row>
    </fieldset>

    <!-- TODO: is this question that different from the first? -->
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodPlan"
      label="J'informe sur la qualité nutritionnelle des repas"
      :readonly="readonly"
      :disabled="readonly"
    />

    <p class="text-left mt-6 mb-2">Lien vers le support de communication</p>
    <v-text-field
      :rules="[validators.urlOrEmpty]"
      solo
      v-model="diagnostic.communicationSupportUrl"
      placeholder="https://"
      validate-on-blur
      :readonly="readonly"
      :disabled="readonly"
    ></v-text-field>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      communicationFrequencies: [
        {
          label: "Régulièrement au cours de l’année",
          value: "REGULARLY",
        },
        {
          label: "Une fois par an",
          value: "YEARLY",
        },
        {
          label: "Moins d'une fois par an",
          value: "LESS_THAN_YEARLY",
        },
      ],
      communicationSupports: [
        {
          label: "Par affichage sur le lieu de restauration",
          value: "DISPLAY",
        },
        {
          label: "Par voie électronique (envoi d’e-mail aux convives, sur site internet ou intranet (mairie, pronote))",
          value: "DIGITAL",
        },
      ],
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

<style scoped>
fieldset {
  border: none;
}
</style>
