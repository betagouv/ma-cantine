<template>
  <div>
    <div class="mb-16" v-if="displayPurchaseHints && purchasesSummary.valueTotalHt > 0">
      <DsfrCallout icon="$money-euro-box-fill">
        <div>
          <p>
            Vous avez renseigné un total de
            <span class="font-weight-bold">{{ toCurrency(purchasesSummary.valueTotalHt) }}</span>
            d'achats en {{ diagnostic.year }}. Voulez-vous compléter votre bilan avec les montants de ces achats ?
          </p>
          <v-btn outlined color="primary" @click="autofillWithPurchases">Compléter avec mes achats</v-btn>
        </div>
      </DsfrCallout>
    </div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <DsfrCurrencyField
      v-model.number="payload.valueTotalHt"
      :rules="[validators.greaterThanZero, validators.decimalPlaces(2)]"
      validate-on-blur
      @blur="updatePayload"
      :error="hasError"
      label="Total (en € HT) de tous mes achats alimentaires"
      ref="totalField"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="payload.valueTotalHt"
      @autofill="onPurchaseAutofill"
      purchaseType="totaux"
      :amount="purchasesSummary.valueTotalHt"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />
    <ErrorHelper
      v-if="hasError || errorHelperUsed"
      class="mt-8"
      :showFields="errorHelperFields"
      :errorFields="erroringFields"
      :diagnostic="payload"
      @field-update="errorUpdate"
      :purchasesSummary="purchasesSummary"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import FormErrorCallout from "@/components/FormErrorCallout"
import DsfrCallout from "@/components/DsfrCallout"
import { toCurrency } from "@/utils"
import validators from "@/validators"

const DEFAULT_TOTAL_ERROR = "Le total doit être plus que la somme des valeurs par label"

export default {
  name: "QualityTotalStep",
  components: { DsfrCurrencyField, PurchaseHint, ErrorHelper, FormErrorCallout, DsfrCallout },
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
      errorHelperUsed: false,
      errorHelperFields: [],
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
    erroringFields() {
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
    toCurrency,
    checkTotal() {
      if (this.payload.valueTotalHt < 0) {
        return // this error is handled by vuetify validation
      }

      this.totalErrorMessage = null
      this.meatPoultryErrorMessage = null
      this.fishErrorMessage = null
      this.totalFamiliesErrorMessage = null

      const d = this.payload
      const sumEgalim = this.sumAllEgalim()
      const total = d.valueTotalHt
      const totalMeatPoultry = d.valueMeatPoultryHt
      const totalFish = d.valueFishHt
      const totalFamilies = totalMeatPoultry + totalFish

      if (sumEgalim > total) {
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${toCurrency(sumEgalim || 0)}`
        if (!this.diagnostic.diagnosticType || this.diagnostic.diagnosticType === "SIMPLE") {
          this.errorHelperFields.push(
            ...["valueBioHt", "valueSustainableHt", "valueEgalimOthersHt", "valueExternalityPerformanceHt"]
          )
        }
      }
      if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
        this.errorHelperFields.push(...["valueMeatPoultryHt", "valueFishHt"])
      } else {
        if (totalMeatPoultry > total) {
          this.meatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
            totalMeatPoultry
          )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
          this.errorHelperFields.push("valueMeatPoultryHt")
        }
        if (totalFish > total) {
          this.fishErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
            totalFish
          )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
          this.errorHelperFields.push("valueFishHt")
        }
      }
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
    errorUpdate() {
      this.errorHelperUsed = true
      this.checkTotal()
    },
    onPurchaseAutofill() {
      this.updatePayload()
      this.$nextTick(this.$refs.totalField.validate)
    },
    autofillWithPurchases() {
      Object.assign(this.payload, { diagnosticType: "COMPLETE" }, this.purchasesSummary)
      this.$emit("tunnel-autofill", {
        payload: this.payload,
        message: {
          status: "success",
          message: "Vos achats on été rapportés dans votre bilan.",
        },
      })
    },
  },
  mounted() {
    this.checkTotal()
  },
}
</script>
