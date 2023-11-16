<template>
  <div>
    <DsfrCurrencyField
      v-model.number="payload.valueTotalHt"
      @blur="updatePayload"
      label="Total (en € HT) de tous mes achats alimentaires"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="payload.valueTotalHt"
      purchaseType="totaux"
      :amount="purchasesSummary.valueTotalHt"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"

export default {
  name: "QualityTotalStep",
  components: { DsfrCurrencyField, PurchaseHint },
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
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
  },
  methods: {
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload })
    },
  },
}
</script>
