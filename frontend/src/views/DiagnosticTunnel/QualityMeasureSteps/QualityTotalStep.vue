<template>
  <div>
    <div v-if="hasError">
      <DsfrCallout v-for="message in errorMessages" :key="message" color="red lighten-1">
        <p class="ma-0">{{ message }}</p>
      </DsfrCallout>
    </div>
    <DsfrCurrencyField
      v-model.number="payload.valueTotalHt"
      :error="hasError"
      label="Total (en € HT) de tous mes achats alimentaires"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="payload.valueTotalHt"
      purchaseType="totaux"
      :amount="purchasesSummary.valueTotalHt"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />
    <ErrorHelper
      :class="`mt-8 ${hasError ? '' : 'd-none'}`"
      :showFields="errorHelperFields"
      :diagnostic="payload"
      @check-total="checkTotal"
      :purchasesSummary="purchasesSummary"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper.vue"
import DsfrCallout from "@/components/DsfrCallout"
import { toCurrency } from "@/utils"

const DEFAULT_TOTAL_ERROR = "Le total doit être plus que la somme des valeurs par label"
const DEFAULT_MEAT_POULTRY_TOTAL_ERROR =
  "Le total des achats viandes et volailles ne peut pas excéder le total des achats"
const DEFAULT_FISH_TOTAL_ERROR =
  "Le total des achats poissons, produits de la mer et de l'aquaculture ne peut pas excéder le total des achats"

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
      totalMeatPoultryError: false,
      totalFishError: false,
      totalError: false,
      totalFamiliesError: false,
      totalErrorMessage: null,
      meatPoultryErrorMessage: null,
      fishErrorMessage: null,
      totalFamiliesErrorMessage: null,
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
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
    errorHelperFields() {
      const fields = []
      if (this.totalError)
        fields.push(...["valueBioHt", "valueSustainableHt", "valueEgalimOthersHt", "valueExternalityPerformanceHt"])
      if (this.totalMeatPoultryError) fields.push("valueMeatPoultryHt")
      if (this.totalFishError) fields.push("valueFishHt")
      if (this.totalFamiliesError) fields.push(...["valueMeatPoultryHt", "valueFishHt"])
      return fields
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      const d = this.payload
      const sumEgalim = this.sumAllEgalim()
      const total = d.valueTotalHt
      const totalMeatPoultry = d.valueMeatPoultryHt
      const totalFish = d.valueFishHt
      const totalFamilies = totalMeatPoultry + totalFish

      this.totalError = sumEgalim > total
      this.totalMeatPoultryError = totalMeatPoultry > total
      this.totalFishError = totalFish > total
      this.totalFamiliesError = totalFamilies > total

      if (this.totalError) {
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${toCurrency(sumEgalim || 0)}`
      } else this.totalErrorMessage = null
      if (this.totalMeatPoultryError) {
        this.meatPoultryErrorMessage = `${DEFAULT_MEAT_POULTRY_TOTAL_ERROR}`
      } else this.meatPoultryErrorMessage = null
      if (this.totalFishError) {
        this.fishErrorMessage = `${DEFAULT_FISH_TOTAL_ERROR}`
      } else this.fishErrorMessage = null
      if (this.totalFamiliesError) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
      } else this.totalFamiliesErrorMessage = null

      return [this.totalError, this.totalMeatPoultryError, this.totalFishError, this.totalFamiliesError].every(
        (x) => !x
      )
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
  },
  watch: {
    payload: {
      handler() {
        this.updatePayload()
      },
      deep: true,
    },
  },
  mounted() {
    this.checkTotal()
  },
}
</script>
