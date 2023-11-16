<template>
  <div>
    <DsfrCurrencyField
      v-model.number="payload.valueTotalHt"
      @blur="updatePayload"
      label="Total (en € HT) de tous mes achats alimentaires"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"

export default {
  name: "QualityTotalStep",
  components: { DsfrCurrencyField },
  props: {
    diagnostic: {
      type: Object,
      required: true,
    },
    payload: {
      type: Object,
      required: true,
    },
  },
  methods: {
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload })
    },
  },
}
</script>
