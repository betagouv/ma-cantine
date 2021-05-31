<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.communicatesOnFoodPlan"
      label="Je communique sur la mise en place d'un plan alimentaire"
    />

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

    <p class="text-left mt-6 mb-2">Lien vers le support de communication</p>
    <v-text-field
      hide-details="auto"
      :rules="[validators.isUrlOrEmpty]"
      solo
      v-model="diagnostic.communicationSupportUrl"
      placeholder="https://"
      validate-on-blur
    ></v-text-field>
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
      communicationSupports: [
        {
          label: "Envoi d'e-mail aux convives ou à leurs représentants",
          value: "EMAIL",
        },
        {
          label: "Par affichage sur le lieu de restauration",
          value: "DISPLAY",
        },
        {
          label: "Sur site internet ou intranet (mairie, cantine)",
          value: "WEBSITE",
        },
        {
          label: "Autres moyens d'affichage et de communication électronique",
          value: "OTHER",
        },
      ],
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
}
</script>
