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
          @blur="$emit('field-update')"
          :error="hasError(field.name)"
          class="mt-2"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic[field.name]"
          @autofill="$emit('field-update')"
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
import Constants from "@/constants"
import { capitalise, getCharacteristicFromField } from "@/utils"

const FISH = "poissons, produits de la mer et de l'aquaculture"
const MEAT = "viandes et volailles"

const SIMPLE_FIELDS = [
  {
    name: "valueTotalHt",
    label: "La valeur totale (en € HT) de mes achats alimentaires",
    purchaseType: "totaux",
  },
  {
    name: "valueBioHt",
    label: "La valeur (en € HT) de mes achats Bio ou en conversion Bio",
    purchaseType: "bio",
  },
  {
    name: "valueSustainableHt",
    label: "La valeur (en € HT) de mes achats SIQO (Label Rouge, AOC / AOP, IGP, STG)",
    purchaseType: "SIQO",
  },
  {
    name: "valueEgalimOthersHt",
    label: "La valeur (en € HT) des autres achats EGalim",
    purchaseType: "« autre EGalim »",
  },
  {
    name: "valueExternalityPerformanceHt",
    label:
      "Critères d'achat : La valeur (en € HT) de mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis sur la base de leurs performances en matière environnementale.",
    purchaseType: "« critères d'achat »",
  },
  {
    name: "valueMeatPoultryHt",
    label: "La valeur totale (en € HT) de mes achats en viandes et volailles fraiches ou surgelées",
    purchaseType: "totaux viandes et volailles",
  },
  {
    name: "valueMeatPoultryEgalimHt",
    label: "La valeur (en € HT) de mes achats EGalim en viandes et volailles fraiches ou surgelées",
    purchaseType: "viandes et volailles EGalim",
  },
  {
    name: "valueMeatPoultryFranceHt",
    label: "La valeur (en € HT) de mes achats provenance France en viandes et volailles fraiches ou surgelées",
    purchaseType: "viandes et volailles provenance France",
  },
  {
    name: "valueFishHt",
    label: "La valeur totale (en € HT) de mes achats en poissons, produits de la mer et de l'aquaculture",
    purchaseType: "totaux de poissons, produits de la mer et de l'aquaculture",
  },
  {
    name: "valueFishEgalimHt",
    label: "La valeur (en € HT) de mes achats EGalim en poissons, produits de la mer et de l'aquaculture",
    purchaseType: "poissons, produits de la mer et de l'aquaculture EGalim",
  },
]

export default {
  name: "ErrorHelper",
  components: { DsfrCurrencyField, PurchaseHint },
  props: {
    showFields: {
      type: Array,
      default: () => [],
    },
    errorFields: {
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
      fields: SIMPLE_FIELDS.concat(this.completeTdFields()),
      originalDiagnostic: JSON.parse(JSON.stringify(this.diagnostic)),
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    // maybe move decision to filter fields to just the defined ones here
    fieldsToShow() {
      return this.fields.filter((field) => this.showField(field.name))
    },
  },
  methods: {
    showField(fieldName) {
      return this.showFields.indexOf(fieldName) > -1 && !!this.originalDiagnostic[fieldName]
    },
    hasError(fieldName) {
      return this.errorFields.indexOf(fieldName) > -1
    },
    completeTdFields() {
      const fishField = "valueProduitsDeLaMer"
      const meatField = "valueViandesVolailles"
      const tdGroups = Constants.TeledeclarationCharacteristicGroups
      const meatFields = []
      const fishFields = []
      for (let groupIdx in tdGroups) {
        const group = tdGroups[groupIdx]
        for (let idx in group.fields) {
          const field = group.fields[idx]
          let family = "Inconnu"
          let characteristic = "Inconnu"
          if (field.startsWith(fishField)) {
            family = FISH
            characteristic = getCharacteristicFromField(field, fishField, group).text
            fishFields.push({
              name: field,
              label: capitalise(`${family} : ${characteristic}`),
              purchaseType: `${family} « ${characteristic} »`,
            })
          } else if (field.startsWith(meatField)) {
            family = MEAT
            characteristic = getCharacteristicFromField(field, meatField, group).text
            meatFields.push({
              name: field,
              label: capitalise(`${family} : ${characteristic}`),
              purchaseType: `${family} « ${characteristic} »`,
            })
          }
        }
      }
      return meatFields.concat(fishFields)
    },
  },
}
</script>
