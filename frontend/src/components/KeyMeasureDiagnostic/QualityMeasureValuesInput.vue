<template>
  <fieldset class="d-flex flex-column">
    <legend class="my-2">{{ label }}</legend>

    <label :for="'total-' + diagnostic.year" class="body-2 mb-1 mt-2">...total</label>
    <v-text-field
      :id="'total-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[
        validators.nonNegativeOrEmpty,
        validators.gteSum([diagnostic.valueBioHt, diagnostic.valueSustainableHt], totalErrorMessage),
      ]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :messages="totalError ? [totalErrorMessage] : undefined"
      :error="totalError"
      @blur="totalError = false"
    ></v-text-field>
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueTotalHt"
      @autofill="checkTotal"
      purchaseType="totaux"
      :amount="purchasesSummary.total"
    />

    <label :for="'bio-' + diagnostic.year" class="body-2 mb-1 mt-4">...en produits bio</label>
    <v-text-field
      :id="'bio-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueBioHt"
      :readonly="readonly"
      :disabled="readonly"
      @blur="checkTotal"
    ></v-text-field>

    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueBioHt"
      @autofill="checkTotal"
      purchaseType="bio"
      :amount="purchasesSummary.bio"
    />

    <label :for="'sustainable-' + diagnostic.year" class="body-2 mb-1 mt-4">
      ...en autres produits de qualité et durables (hors bio)
    </label>
    <v-text-field
      :id="'sustainable-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueSustainableHt"
      :readonly="readonly"
      :disabled="readonly"
      @blur="checkTotal"
    ></v-text-field>
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueSustainableHt"
      @autofill="checkTotal"
      purchaseType="qualité et durable"
      :amount="purchasesSummary.sustainable"
    />
  </fieldset>
</template>

<script>
import validators from "@/validators"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"

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
  components: { PurchaseHint },
  data() {
    return {
      totalError: false,
      totalErrorMessage: "Le totale ne peut pas être moins que le somme des valeurs suivantes",
    }
  },
  computed: {
    validators() {
      return validators
    },
    diagnostic() {
      return this.originalDiagnostic
    },
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x) && !this.readonly
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
