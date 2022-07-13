<template>
  <div>
    <QualityMeasureValuesInput
      :originalDiagnostic="diagnostic"
      label="La valeur (en HT) de mes achats alimentaires..."
      :readonly="hasActiveTeledeclaration"
      :purchasesSummary="purchasesSummary"
    />
  </div>
</template>

<script>
import QualityMeasureValuesInput from "@/components/KeyMeasureDiagnostic/QualityMeasureValuesInput"
import validators from "@/validators"

export default {
  name: "SimplifiedQualityValues",
  props: {
    originalDiagnostic: Object,
    purchasesSummary: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    QualityMeasureValuesInput,
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
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
</style>
