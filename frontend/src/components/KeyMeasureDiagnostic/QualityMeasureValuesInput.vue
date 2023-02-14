<template>
  <fieldset class="d-flex flex-column">
    <legend class="my-2 body-2">{{ label }}</legend>

    <label :for="'total-' + diagnostic.year" class="body-2 mb-1 mt-2">...total</label>
    <DsfrCurrencyField
      :id="'total-' + diagnostic.year"
      :rules="[
        validators.nonNegativeOrEmpty,
        validators.decimalPlaces(2),
        validators.gteSum([diagnostic.valueBioHt, diagnostic.valueSustainableHt], totalErrorMessage),
      ]"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :messages="totalError ? [totalErrorMessage] : undefined"
      :error="totalError"
      @blur="totalError = false"
    />

    <label :for="'bio-' + diagnostic.year" class="body-2 mb-1 mt-4">...en produits bio</label>
    <DsfrCurrencyField
      :id="'bio-' + diagnostic.year"
      :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
      v-model.number="diagnostic.valueBioHt"
      :readonly="readonly"
      :disabled="readonly"
      @blur="checkTotal"
    />

    <label :for="'sustainable-' + diagnostic.year" class="body-2 mb-1 mt-4">
      ...en autres produits de qualité et durables (hors bio)
    </label>
    <DsfrCurrencyField
      :id="'sustainable-' + diagnostic.year"
      :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
      v-model.number="diagnostic.valueSustainableHt"
      :readonly="readonly"
      :disabled="readonly"
      @blur="checkTotal"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueSustainableHt"
      @autofill="checkTotal"
      purchaseType="qualité et durable"
      :amount="purchasesSummary.siqo"
    />
  </fieldset>
</template>

<script>
import validators from "@/validators"
import DsfrCurrencyField from "@/components/DsfrCurrencyField"

export default {
  props: {
    label: String,
    originalDiagnostic: Object,
    purchasesSummary: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: { DsfrCurrencyField },
  data() {
    return {
      totalError: false,
      totalErrorMessage: "Le totale ne peut pas être moins que la somme des valeurs suivantes",
    }
  },
  computed: {
    validators() {
      return validators
    },
    diagnostic() {
      return this.originalDiagnostic
    },
  },
  methods: {
    checkTotal() {
      const result = validators.gteSum(
        [this.diagnostic.valueBioHt, this.diagnostic.valueSustainableHt],
        this.totalErrorMessage
      )(this.diagnostic.valueTotalHt)
      this.totalError = result !== true
    },
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
</style>
