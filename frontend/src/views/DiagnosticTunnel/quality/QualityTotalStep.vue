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
  },
  data() {
    return {
      payload: {
        valueTotalHt: this.diagnostic.valueTotalHt,
      },
      formIsValid: true, // TODO
    }
  },
  methods: {
    updatePayload() {
      this.$emit("updatePayload", { payload: this.payload, formIsValid: this.formIsValid })
    },
  },
}
</script>
