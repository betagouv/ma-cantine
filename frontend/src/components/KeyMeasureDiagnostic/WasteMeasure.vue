<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWasteDiagnostic"
      label="J'ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWastePlan"
      label="J'ai mis en place un plan d’actions adapté au diagnostic réalisé"
    />

    <!-- TODO: a11y label and checkboxes -->
    <p class="text-left mt-6 mb-2">J'ai réalisé des actions de lutte contre le gaspillage alimentaire :</p>

    <v-checkbox
      hide-details="auto"
      class="ml-8"
      v-model="diagnostic.wasteActions"
      v-for="action in wasteActions"
      :key="action.value"
      :value="action.value"
      :label="action.label"
    />
    <v-row align="center" class="ml-8 mt-2 mr-2">
      <v-checkbox v-model="otherActionEnabled" hide-details class="shrink mt-0"></v-checkbox>
      <v-text-field :disabled="!otherActionEnabled" label="Autre : donnez plus d'informations"></v-text-field>
    </v-row>

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWasteMeasures"
      label="J'ai réalisé des mesures de mon gaspillage alimentaire"
    />
    <v-expand-transition>
      <div v-if="diagnostic.hasWasteMeasures" class="mt-4">
        <v-text-field class="mx-8" label="Reste de pain" suffix="kg/an"></v-text-field>
        <v-text-field class="mx-8" label="Reste plateau" suffix="kg/an"></v-text-field>
        <v-text-field class="mx-8" label="Reste en production (non servi)" suffix="kg/an"></v-text-field>
        <v-text-field class="mx-8" label="Reste de composantes (entrée, plat dessert...)" suffix="kg/an"></v-text-field>
      </div>
    </v-expand-transition>

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasDonationAgreement"
      label="Je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire"
    />
    <p class="text-left mx-8 mt-2 explanation">
      Seulement les cantines qui fabriquent plus de 3 000 repas par jour en moyenne doivent proposer des conventions.
    </p>

    <v-expand-transition>
      <div v-if="diagnostic.hasDonationAgreement" class="my-4">
        <v-text-field class="mx-8" label="Fréquence de dons" suffix="dons/an"></v-text-field>
        <v-text-field class="mx-8" label="Quantité des denrées données" suffix="par an"></v-text-field>
        <v-text-field class="mx-8" label="Type de denrées données"></v-text-field>
      </div>
    </v-expand-transition>

    <v-textarea label="Autres commentaires" outlined rows="3"></v-textarea>
  </div>
</template>

<script>
export default {
  props: {
    diagnostic: Object,
  },
  data() {
    return {
      wasteActions: [
        {
          label: "Pré-inscription des convives obligatoire",
          value: "INSCRIPTION",
        },
        {
          label: "Sensibilisation par affichage ou autre média",
          value: "AWARENESS",
        },
        {
          label: "Formation / information du personnel de restauration",
          value: "TRAINING",
        },
        {
          label: "Réorganisation de la distribution des composantes du repas",
          value: "DISTRIBUTION",
        },
        {
          label: "Choix des portions (grande faim, petite faim)",
          value: "PORTIONS",
        },
        {
          label: "Réutilisation des restes de préparation / surplus",
          value: "REUSE",
        },
      ],
      otherActionEnabled: false,
    }
  },
}
</script>

<style scoped>
.explanation {
  color: grey;
  font-size: 0.8em;
}
</style>
