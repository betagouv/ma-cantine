<template>
  <div>
    <div v-if="hasError">
      <DsfrCallout v-if="errorMessages.length > 1" color="red lighten-1">
        <p class="ma-0">Merci de vérifier les erreurs ci dessous :</p>
        <ul>
          <li v-for="message in errorMessages" :key="message">{{ message }}</li>
        </ul>
      </DsfrCallout>
      <DsfrCallout v-else color="red lighten-1">
        <p class="ma-0">{{ errorMessages[0] }}</p>
      </DsfrCallout>
    </div>
    <DsfrCurrencyField
      v-model.number="payload.valueTotalHt"
      :rules="[validators.greaterThanZero, validators.decimalPlaces(2)]"
      @blur="checkTotal"
      :error="hasError"
      label="Total (en € HT) de tous mes achats alimentaires"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="payload.valueTotalHt"
      @autofill="checkTotal"
      purchaseType="totaux"
      :amount="purchasesSummary.valueTotalHt"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />
    <ErrorHelper
      v-if="errorHelperFields.length"
      class="mt-8"
      :showFields="errorHelperFields"
      :diagnostic="diagnostic"
      @update-payload="updatePayloadFromComponent"
      :purchasesSummary="purchasesSummary"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import DsfrCallout from "@/components/DsfrCallout"
import { toCurrency } from "@/utils"
import validators from "@/validators"

const DEFAULT_TOTAL_ERROR = "Le total doit être plus que la somme des valeurs par label"

export default {
  name: "QualityTotalStep",
  components: { DsfrCurrencyField, PurchaseHint, ErrorHelper, DsfrCallout },
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
    return {
      totalErrorMessage: null,
      meatPoultryErrorMessage: null,
      fishErrorMessage: null,
      totalFamiliesErrorMessage: null,
      errorHelperFields: [],
      errorHelperUsed: false,
    }
  },
  computed: {
    validators() {
      return validators
    },
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    totalMeatPoultryError() {
      return !!this.totalMeatPoultryErrorMessage
    },
    totalFishError() {
      return !!this.totalFishErrorMessage
    },
    totalError() {
      return !!this.totalErrorMessage
    },
    totalFamiliesError() {
      return !!this.totalFamiliesErrorMessage
    },
    errorMessages() {
      return [
        this.totalErrorMessage,
        this.meatPoultryErrorMessage,
        this.fishErrorMessage,
        this.totalFamiliesErrorMessage,
      ].filter((x) => !!x)
    },
    hasError() {
      return [this.totalMeatPoultryError, this.totalFishError, this.totalError, this.totalFamiliesError].some(
        (x) => !!x
      )
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    updatePayloadFromComponent(componentPayload) {
      this.errorHelperUsed = true
      this.$set(this, "payload", Object.assign(this.payload, componentPayload))
      this.checkTotal()
    },
    checkTotal() {
      if (!this.payload.valueTotalHt || this.payload.valueTotalHt < 0) return
      const d = this.payload
      const sumEgalim = this.sumAllEgalim()
      const total = d.valueTotalHt
      const totalMeatPoultry = d.valueMeatPoultryHt
      const totalFish = d.valueFishHt
      const totalFamilies = totalMeatPoultry + totalFish

      if (sumEgalim > total) {
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${toCurrency(sumEgalim || 0)}`
      } else this.totalErrorMessage = null
      if (totalMeatPoultry > total) {
        this.meatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalMeatPoultry
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
      } else this.meatPoultryErrorMessage = null
      if (totalFish > total) {
        this.fishErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
          totalFish
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
      } else this.fishErrorMessage = null
      if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
      } else this.totalFamiliesErrorMessage = null

      this.addErrorHelperFields()
    },
    sumAllEgalim() {
      const d = this.payload
      const egalimValues = [d.valueBioHt, d.valueSustainableHt, d.valueExternalityPerformanceHt, d.valueEgalimOthersHt]
      let total = 0
      egalimValues.forEach((val) => {
        total += parseFloat(val) || 0
      })
      return total
    },
    addErrorHelperFields() {
      if (!this.errorHelperUsed) this.$set(this, "errorHelperFields", [])
      if (this.totalError)
        this.errorHelperFields.push(
          ...["valueBioHt", "valueSustainableHt", "valueEgalimOthersHt", "valueExternalityPerformanceHt"]
        )
      if (this.totalMeatPoultryError) this.errorHelperFields.push("valueMeatPoultryHt")
      if (this.totalFishError) this.errorHelperFields.push("valueFishHt")
      if (this.totalFamiliesError) this.errorHelperFields.push(...["valueMeatPoultryHt", "valueFishHt"])
    },
  },
  mounted() {
    this.checkTotal()
  },
}
</script>
