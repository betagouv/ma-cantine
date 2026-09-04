<template>
  <DsfrTextField
    hide-details="auto"
    min="0"
    :rules="$attrs.rules || [validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
    :validate-on-blur="$attrs.validateOnBlur"
    :validate="$attrs.validate"
    :placeholder="$attrs.placeholder || 'Je ne sais pas'"
    suffix="€ HT"
    v-bind="$attrs"
    v-on="$listeners"
    ref="text-field"
  />
</template>

<script>
import DsfrTextField from "@/components/DsfrTextField"
import validators from "@/validators"

export default {
  inheritAttrs: false,
  components: { DsfrTextField },
  computed: {
    validators() {
      return validators
    },
  },
  methods: {
    validate() {
      return this.$refs["text-field"].validate()
    },
    resetValidation() {
      return this.$refs["text-field"].resetValidation()
    },
  },
}
</script>
