<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodQuality"
      label="J’informe mes convives sur la part de produits de qualité et durables, entrant dans la composition des repas servis, et sur les démarches d’acquisition de produits issus du commerce équitable"
    />

    <p class="text-left mt-6 mb-2">
      Les actions ci-dessous sont des exemples, vous pouvez indiquer si ce sont des actions que vous avez mises en place
      ou préciser ou ajouter ou d’autres actions :
    </p>
    <v-checkbox
      hide-details="auto"
      class="ml-8"
      v-model="diagnostic.communicationContents"
      v-for="support in communicationContents"
      :key="support.value"
      :value="support.value"
      :label="support.label"
    />
    <v-row align="center" class="ml-8 mt-2 mr-2">
      <v-checkbox v-model="otherContentEnabled" hide-details class="shrink mt-0"></v-checkbox>
      <v-text-field :disabled="!otherContentEnabled" label="Autre : donnez plus d'informations"></v-text-field>
    </v-row>

    <p class="text-left mt-6 mb-2">Je fais cette information :</p>
    <v-radio-group v-model="diagnostic.communicationFrequency">
      <v-radio
        class="ml-8"
        v-for="item in communicationFrequencies"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      ></v-radio>
    </v-radio-group>

    <p class="text-left mt-6 mb-2">J'informe sur la qualité des approvisionnements :</p>
    <v-checkbox
      hide-details="auto"
      class="ml-8"
      v-model="diagnostic.communicationSupports"
      v-for="support in communicationSupports"
      :key="support.value"
      :value="support.value"
      :label="support.label"
    />
    <v-row align="center" class="ml-8 mt-2 mr-2">
      <v-checkbox v-model="otherSupportEnabled" hide-details class="shrink mt-0"></v-checkbox>
      <v-text-field :disabled="!otherSupportEnabled" label="Autre : donnez plus d'informations"></v-text-field>
    </v-row>

    <p class="text-left mt-4"><u>Information sur la qualité nutritionnelle des repas</u></p>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodPlan"
      label="J'informe sur la qualité nutritionnelle des repas"
    />
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  props: {
    diagnostic: Object,
  },
  data() {
    return {
      communicationContents: [
        {
          label: "L’information porte sur la part en valeur d’achat (€) des produits servis",
          value: "VALUE_OF_PRODUCTS",
        },
        {
          label: "L’information porte sur la quantité de ces produits servis",
          value: "QUANTITY",
        },
        {
          label: "L’information porte sur le nombre de composantes servis",
          value: "NUMBER",
        },
      ],
      communicationFrequencies: [
        {
          label: "Régulièrement au cours de l’année",
          value: "REGULARLY",
        },
        {
          label: "Une fois par an",
          value: "ONCE",
        },
        {
          label: "Moins d'une fois par an",
          value: "LESS_THAN_ONCE",
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
      otherContentEnabled: false,
      otherSupportEnabled: false,
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
}
</script>
