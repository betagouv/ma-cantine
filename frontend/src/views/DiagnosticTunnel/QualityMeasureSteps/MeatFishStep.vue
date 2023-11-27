<template>
  <div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col cols="12" md="8">
        <div class="d-block d-sm-flex align-center">
          <div class="d-flex">
            <v-icon size="30" color="brown">
              mdi-food-steak
            </v-icon>
            <v-icon size="30" color="brown">
              mdi-food-drumstick
            </v-icon>
          </div>
          <label class="fr-text ml-4" :for="'meat-poultry-' + diagnostic.year">
            La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
          </label>
        </div>
        <DsfrCurrencyField
          :id="'meat-poultry-' + diagnostic.year"
          v-model.number="payload.valueMeatPoultryHt"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="hasMeatError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryHt"
          @autofill="checkTotal"
          purchaseType="totaux viandes et volailles"
          :amount="purchasesSummary.valueMeatPoultryHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
        <!-- Poissons -->
        <div class="d-block d-sm-flex align-center mt-8">
          <div class="d-flex">
            <v-icon size="30" color="blue">
              mdi-fish
            </v-icon>
          </div>
          <label class="fr-text ml-4" :for="'fish-' + diagnostic.year">
            La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total
          </label>
        </div>
        <DsfrCurrencyField
          :id="'fish-' + diagnostic.year"
          v-model.number="payload.valueFishHt"
          :error="hasFishError"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueFishHt"
          @autofill="checkTotal"
          purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
          :amount="purchasesSummary.valueFishHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
    </v-row>
    <ErrorHelper
      v-if="hasError || errorHelperUsed"
      :showFields="errorHelperFields"
      :errorFields="erroringFields"
      :diagnostic="payload"
      :purchasesSummary="purchasesSummary"
      @field-update="errorUpdate"
      class="mt-8"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import FormErrorCallout from "@/components/FormErrorCallout"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import Constants from "@/constants"

export default {
  name: "MeatFishStep",
  components: { DsfrCurrencyField, FormErrorCallout, PurchaseHint, ErrorHelper },
  props: {
    diagnostic: {
      type: Object,
      required: true,
    },
    payload: {
      type: Object,
      required: true,
    },
    purchasesSummary: {
      type: Object,
    },
  },
  data() {
    const tdGroups = Constants.TeledeclarationCharacteristicGroups

    const meatLawFields = []
    const fishLawFields = []
    const lawFields = tdGroups.egalim.fields.concat(tdGroups.nonEgalim.fields)
    lawFields.forEach((field) => {
      if (field.startsWith("valueViandesVolailles")) meatLawFields.push(field)
      else if (field.startsWith("valueProduitsDeLaMer")) fishLawFields.push(field)
    })
    const meatOutsideLawFields = []
    const fishOutsideLawFields = []
    const outsideLawFields = [...tdGroups.outsideLaw.fields]
    outsideLawFields.forEach((field) => {
      if (field.startsWith("valueViandesVolailles")) meatOutsideLawFields.push(field)
      else if (field.startsWith("valueProduitsDeLaMer")) fishOutsideLawFields.push(field)
    })

    return {
      errorHelperFields: [],
      errorHelperUsed: false,
      totalField: "valueTotalHt",
      meatLawFields,
      meatOutsideLawFields,
      fishLawFields,
      fishOutsideLawFields,
      meatTotalError: false,
      fishTotalError: false,
      combinedTotalError: false,
      meatLawSubtotalError: false,
      meatOutsideLawSubtotalErrors: [],
      fishLawSubtotalError: false,
      fishOutsideLawSubtotalErrors: [],
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
    erroringFields() {
      const fields = []
      if (this.meatTotalError) fields.push(this.totalField)
      if (this.fishTotalError) fields.push(this.totalField)
      if (this.combinedTotalError) fields.push(this.totalField)
      if (this.meatLawSubtotalError) fields.push(...this.defined(this.meatLawFields))
      // if (this.meatOutsideLawSubtotalError) fields.push(...this.defined(this.meatOutsideLawFields))
      if (this.fishLawSubtotalError) fields.push(...this.defined(this.fishLawFields))
      // if (this.fishOutsideLawSubtotalError) fields.push(...this.defined(this.fishOutsideLawFields))
      return fields
    },
    hasError() {
      return this.erroringFields.length
    },
    hasMeatError() {
      return (
        this.meatTotalError || this.combinedTotalError || this.meatLawSubtotalError // || this.meatOutsideLawSubtotalError
      )
    },
    hasFishError() {
      return (
        this.fishTotalError || this.combinedTotalError || this.fishLawSubtotalError // || this.fishOutsideLawSubtotalError
      )
    },
    errorMessages() {
      return [
        this.meatTotalErrorMessage,
        this.fishTotalErrorMessage,
        this.combinedTotalErrorMessage,
        this.meatLawSubtotalErrorMessage,
        // this.meatOutsideLawSubtotalErrorMessage,
        this.fishLawSubtotalErrorMessage,
        // this.fishOutsideLawSubtotalErrorMessage,
      ].filter((x) => !!x)
    },
    // error messages text
    meatTotalErrorMessage() {
      if (!this.meatTotalError) return null
      return "meatTotalError"
    },
    fishTotalErrorMessage() {
      if (!this.fishTotalError) return null
      return "fishTotalError"
    },
    combinedTotalErrorMessage() {
      if (!this.combinedTotalError) return null
      return "combinedTotalError"
    },
    meatLawSubtotalErrorMessage() {
      if (!this.meatLawSubtotalError) return null
      return "meatLawSubtotalError"
    },
    // meatOutsideLawSubtotalErrorMessage() {
    //   if (!this.meatOutsideLawSubtotalError) return null
    //   return "meatOutsideLawSubtotalError"
    // },
    fishLawSubtotalErrorMessage() {
      if (!this.fishLawSubtotalError) return null
      return "fishLawSubtotalError"
    },
    // fishOutsideLawSubtotalErrorMessage() {
    //   if (!this.fishOutsideLawSubtotalError) return null
    //   return "fishOutsideLawSubtotalError"
    // },
  },
  methods: {
    checkTotal() {
      this.combinedTotalError = false

      const d = this.payload
      const total = d.valueTotalHt
      const meatTotal = d.valueMeatPoultryHt
      const fishTotal = d.valueFishHt

      if (meatTotal + fishTotal > total) {
        this.combinedTotalError = true
        this.errorHelperFields.push(this.totalField)
      }

      this.checkFamilyTotal("meat")
      this.checkFamilyTotal("fish")
    },
    checkFamilyTotal(family) {
      // family === "meat" or "fish"
      this[`${family}TotalError`] = false
      this[`${family}LawSubtotalError`] = false
      this[`${family}OutsideLawSubtotalError`] = false

      const d = this.payload
      const total = d.valueTotalHt
      const familyTotal = family === "meat" ? d.valueMeatPoultryHt : d.valueFishHt
      if (!familyTotal) return

      if (familyTotal > total) {
        this[`${family}TotalError`] = true
        this.errorHelperFields.push(this.totalField)
      }

      if (this.sum(this[`${family}LawFields`]) > familyTotal) {
        this[`${family}LawSubtotalError`] = true
        this.errorHelperFields.push(...this.defined(this[`${family}LawFields`]))
      }
      this[`${family}OutsideLawSubtotalErrors`] = []
      this[`${family}OutsideLawFields`].forEach((field) => {
        if (d[field] > familyTotal) {
          this[`${family}OutsideLawSubtotalErrors`].push(field)
        }
      })
    },
    errorUpdate() {
      this.errorHelperUsed = true
      this.checkTotal()
    },
    sum(fields) {
      return fields.reduce((acc, field) => acc + (this.payload[field] || 0), 0)
    },
    defined(fields) {
      return fields.filter((field) => !!this.payload[field])
    },
  },
}
</script>
