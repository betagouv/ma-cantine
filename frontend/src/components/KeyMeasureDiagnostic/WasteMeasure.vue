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

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasDonationAgreement"
      label="Si ma cantine fabrique plus de 3 000 repas par jour en moyenne, je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire"
    />

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
    }
  },
}
</script>
