<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodQuality"
      label="J’informe mes convives sur la part de produits de qualité et durables, entrant dans la composition des repas servis, et sur les démarches d’acquisition de produits issus du commerce équitable"
      :readonly="readonly"
      :disabled="readonly"
    />

    <fieldset>
      <legend class="text-left mt-6 mb-2">Je fais cette information :</legend>
      <v-radio-group v-model="diagnostic.communicationFrequency">
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

    <fieldset>
      <legend class="text-left my-2">J'informe sur la qualité des approvisionnements :</legend>
      <v-checkbox
        hide-details="auto"
        class="ml-8"
        v-model="diagnostic.communicationSupports"
        :multiple="true"
        v-for="support in communicationSupports"
        :key="support.value"
        :value="support.value"
        :label="support.label"
        :readonly="readonly"
        :disabled="readonly"
      />
      <v-row align="center" class="ml-8 mt-2 mr-2">
        <v-checkbox
          v-model="otherSupportEnabled"
          hide-details
          class="shrink mt-0"
          :readonly="readonly"
          :disabled="readonly"
        ></v-checkbox>
        <v-text-field
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
