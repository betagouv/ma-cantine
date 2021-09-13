<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWasteDiagnostic"
      label="J'ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire"
      :readonly="readonly"
      :disabled="readonly"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWastePlan"
      label="J'ai mis en place un plan d’actions adapté au diagnostic réalisé"
      :readonly="readonly"
      :disabled="readonly"
    />

    <fieldset class="mt-3 mb-4">
      <legend class="text-left my-3">J'ai réalisé des actions de lutte contre le gaspillage alimentaire :</legend>

      <v-checkbox
        hide-details="auto"
        class="ml-8 mb-3 mt-0"
        v-model="diagnostic.wasteActions"
        :multiple="true"
        v-for="action in wasteActions"
        :key="action.value"
        :value="action.value"
        :label="action.label"
        :readonly="readonly"
        :disabled="readonly"
      />
      <v-row align="center" class="ml-8 mb-3 mt-0 mr-2">
        <v-checkbox
          v-model="otherActionEnabled"
          hide-details
          class="shrink mt-0"
          :readonly="readonly"
          :disabled="readonly"
        ></v-checkbox>
        <v-text-field
          class="my-0 py-0"
          hide-details
          :disabled="!otherActionEnabled || readonly"
          v-model="diagnostic.otherWasteAction"
          label="Autre : donnez plus d'informations"
          :readonly="readonly"
        ></v-text-field>
      </v-row>
    </fieldset>

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWasteMeasures"
      label="J'ai réalisé des mesures de mon gaspillage alimentaire"
      :readonly="readonly"
      :disabled="readonly"
    />
    <v-expand-transition>
      <v-row v-if="diagnostic.hasWasteMeasures" class="mt-4 ml-8">
        <v-col cols="12" md="8" class="pa-0">
          <v-text-field
            v-model="diagnostic.breadLeftovers"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Reste de pain"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          ></v-text-field>
          <v-text-field
            v-model="diagnostic.servedLeftovers"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Reste plateau"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          ></v-text-field>
          <v-text-field
            v-model="diagnostic.unservedLeftovers"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Reste en production (non servi)"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          ></v-text-field>
          <v-text-field
            v-model="diagnostic.sideLeftovers"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Reste de composantes (entrée, plat dessert...)"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-expand-transition>

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasDonationAgreement"
      label="Je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire"
      :readonly="readonly"
      :disabled="readonly"
    />
    <p class="text-left mx-8 mt-2 explanation">
      Seulement les cantines qui fabriquent plus de 3 000 repas par jour en moyenne doivent proposer des conventions.
    </p>

    <v-expand-transition>
      <v-row v-if="diagnostic.hasDonationAgreement" class="my-4 ml-8">
        <v-col cols="12" md="8" class="pa-0">
          <v-text-field
            v-model="diagnostic.donationFrequency"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Fréquence de dons"
            suffix="dons/an"
            :readonly="readonly"
            :disabled="readonly"
          ></v-text-field>
          <v-text-field
            v-model="diagnostic.donationQuantity"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Quantité des denrées données"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          ></v-text-field>
        </v-col>
        <v-col cols="11" class="pa-0">
          <v-text-field
            v-model="diagnostic.donationFoodType"
            label="Type de denrées données"
            :readonly="readonly"
            :disabled="readonly"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-expand-transition>

    <v-textarea
      v-model="diagnostic.otherWasteComments"
      label="Autres commentaires"
      outlined
      rows="3"
      :readonly="readonly"
      :disabled="readonly"
    ></v-textarea>
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
      otherActionEnabled: !!this.diagnostic.otherWasteAction,
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
  watch: {
    otherActionEnabled(val) {
      if (!val) {
        this.diagnostic.otherWasteAction = null
      }
    },
  },
}
</script>

<style scoped>
.explanation {
  color: grey;
  font-size: 0.8em;
}

fieldset {
  border: none;
}
</style>
