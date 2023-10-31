<template>
  <div class="grey--text text--darken-2">
    <p class="mb-1">{{ text }}</p>
    <p class="font-weight-bold" v-if="!value">Je ne sais pas</p>
    <p class="font-weight-bold" v-else-if="Number.isNaN(+value)">{{ value }}</p>
    <p class="font-weight-bold" v-else>{{ toCurrency(+value) }} HT</p>
  </div>
</template>

<script>
import { toCurrency } from "@/utils"

export default {
  name: "QualityDiagnosticValue",
  props: {
    text: String,
    value: [String, Number],
  },
  methods: {
    toCurrency(value) {
      return toCurrency(value)
    },
  },
}
</script>
