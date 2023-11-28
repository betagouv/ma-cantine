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
import { capitalise } from "@/utils"

const FISH = "poissons, produits de la mer et de l'aquaculture"
const MEAT = "viandes et volailles"

const SIMPLE_FIELDS = [
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
      return this.showFields.indexOf(fieldName) > -1
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
        const normalisedGroupCharacteristics = group.characteristics.map((g) => g.toLowerCase().replace(/_/g, ""))
        for (let idx in group.fields) {
          const field = group.fields[idx]
          let family = "Inconnu"
          let characteristic = "Inconnu"
          if (field.startsWith(fishField)) {
            family = FISH
            characteristic = this.characteristicText(group, normalisedGroupCharacteristics, field.split(fishField)[1])
            fishFields.push({
              name: field,
              label: capitalise(`${family} : ${characteristic}`),
              purchaseType: `${family} « ${characteristic} »`,
            })
          } else if (field.startsWith(meatField)) {
            family = MEAT
            characteristic = this.characteristicText(group, normalisedGroupCharacteristics, field.split(meatField)[1])
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
    characteristicText(tdGroup, normalisedGroupCharacteristics, fieldSuffix) {
      const fieldCharacteristic = fieldSuffix.toLowerCase()
      const charIdx = normalisedGroupCharacteristics.indexOf(fieldCharacteristic)
      if (charIdx === -1) return fieldSuffix
      const originalChar = tdGroup.characteristics[charIdx]
      return Constants.TeledeclarationCharacteristics[originalChar].text
    },
  },
}
</script>
