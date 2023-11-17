<template>
  <div>
    <DsfrCallout v-if="totalError" color="red lighten-1">
      <p class="ma-0" v-for="message in errorMessages" :key="message">{{ message }}</p>
    </DsfrCallout>
    <DsfrCurrencyField v-model.number="payload.valueTotalHt" label="Total (en € HT) de tous mes achats alimentaires" />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="payload.valueTotalHt"
      purchaseType="totaux"
      :amount="purchasesSummary.valueTotalHt"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />
    <ErrorHelper
      class="mt-8"
      :showFields="errorHelperFields"
      v-if="totalError"
      :diagnostic="payload"
      @check-total="checkTotal"
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
      totalErrorMessage: null,
      meatPoultryErrorMessage: null,
      fishErrorMessage: null,
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
    errorMessages() {
      return [this.totalErrorMessage, this.meatPoultryErrorMessage, this.fishErrorMessage].filter((x) => !!x)
    },
    hasError() {
      return [this.totalMeatPoultryError, this.totalFishError, this.totalError].some((x) => !!x)
    },
    errorHelperFields() {
      const fields = []
      if (this.totalError)
        fields.push(...["valueBioHt", "valueSustainableHt", "valueEgalimOthersHt", "valueExternalityPerformanceHt"])
      if (this.totalMeatPoultryError) fields.push("valueMeatPoultryHt")
      if (this.totalFishError) fields.push("valueFishHt")
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
      this.totalMeatPoultryError = !this.totalError && (totalMeatPoultry > total || totalFamilies > total)
      this.totalFishError = !this.totalError && (totalFish > total || totalFamilies > total)

      if (this.totalError) {
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${toCurrency(sumEgalim || 0)}`
      }
      if (this.totalMeatPoultryError) {
        this.meatPoultryErrorMessage = `${DEFAULT_MEAT_POULTRY_TOTAL_ERROR}`
      }
      if (this.totalFishError) {
        this.fishErrorMessage = `${DEFAULT_FISH_TOTAL_ERROR}`
      }
      if (!this.totalError && !this.totalMeatPoultryError && !this.totalFishError) {
        this.meatPoultryErrorMessage = this.fishErrorMessage = this.totalErrorMessage = ""
      }

      return [this.totalError, this.totalMeatPoultryError, this.totalFishError].every((x) => !x)
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
}
</script>
