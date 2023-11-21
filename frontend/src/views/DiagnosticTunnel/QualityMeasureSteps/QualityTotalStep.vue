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
import ErrorHelper from "./ErrorHelper"
import DsfrCallout from "@/components/DsfrCallout"
import { toCurrency } from "@/utils"

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
    }
  },
  computed: {
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
