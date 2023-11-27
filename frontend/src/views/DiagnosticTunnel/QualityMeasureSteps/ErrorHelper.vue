<template>
  <v-card outlined>
    <v-card-text class="pb-0 d-flex">
      <v-icon>$error-warning-fill</v-icon>
      <p class="ma-0 ml-2">L'erreur de validation pourrait se trouver dans un de ces champs</p>
    </v-card-text>
    <v-card-text>
      <div v-for="field in fieldsToShow" :key="field.name" class="my-2">
        <label :for="field.name" class="fr-text-sm">
          {{ field.label }}
        </label>

        <DsfrCurrencyField
          :id="field.name"
          v-model.number="diagnostic[field.name]"
          @blur="$emit('check-total')"
          class="mt-2"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic[field.name]"
          @autofill="$emit('check-total')"
          :purchaseType="field.purchaseType"
          :amount="purchasesSummary[field.name]"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"

export default {
  name: "ErrorHelper",
  components: { DsfrCurrencyField, PurchaseHint },
  props: {
    showFields: {
      type: Array,
      default: () => [],
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    purchasesSummary: {
      type: Object,
    },
  },
  data() {
    return {
      fields: [
        {
          name: "valueTotalHt",
          label: "La valeur (en HT) de mes achats alimentaires total",
          purchaseType: "totaux",
        },
        {
          name: "valueBioHt",
          label: "La valeur (en HT) de mes achats Bio ou en conversion Bio",
          purchaseType: "bio",
        },
        {
          name: "valueSustainableHt",
          label: "La valeur (en HT) de mes achats SIQO (Label Rouge, AOC / AOP, IGP, STG)",
          purchaseType: "SIQO",
        },
        {
          name: "valueEgalimOthersHt",
          label: "La valeur (en HT) des autres achats EGAlim",
          purchaseType: "« autre EGAlim »",
        },
        {
          name: "valueExternalityPerformanceHt",
          label:
            "Critères d'achat : La valeur (en HT) de mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis sur la base de leurs performances en matière environnementale.",
          purchaseType: "« critères d'achat »",
        },
        {
          name: "valueMeatPoultryHt",
          label: "La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total",
          purchaseType: "totaux viandes et volailles",
        },
        {
          name: "valueMeatPoultryEgalimHt",
          label: "La valeur (en HT) des mes achats EGAlim en viandes et volailles fraiches ou surgelées",
          purchaseType: "viandes et volailles EGAlim",
        },
        {
          name: "valueMeatPoultryFranceHt",
          label: "La valeur (en HT) des mes achats provenance France en viandes et volailles fraiches ou surgelées",
          purchaseType: "viandes et volailles provenance France",
        },
        {
          name: "valueFishHt",
          label: "La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total",
          purchaseType: "totaux de poissons, produits de la mer et de l'aquaculture",
        },
        {
          name: "valueFishEgalimHt",
          label: "La valeur (en HT) des mes achats EGAlim en poissons, produits de la mer et de l'aquaculture",
          purchaseType: "poissons, produits de la mer et de l'aquaculture EGAlim",
        },
      ],
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    fieldsToShow() {
      return this.fields.filter((field) => this.showField(field.name))
    },
  },
  methods: {
    showField(fieldName) {
      return this.showFields.indexOf(fieldName) > -1
    },
  },
}
</script>
