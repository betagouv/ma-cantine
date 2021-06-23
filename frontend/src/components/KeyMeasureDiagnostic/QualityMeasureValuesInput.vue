<template>
  <div class="d-flex flex-column">
    <!-- TODO: Use text field suffix (euros HT) instead of (en HT) here? -->
    <!-- TODO: Use text field labels instead of separate p tags? -->
    <p>{{ label }}</p>

    <p class="body-2 mb-1 mt-2">...totale</p>
    <v-text-field
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      v-model="diagnostic.valueTotalHt"
    ></v-text-field>

    <p class="body-2 mb-1 mt-4">...en produits bio</p>
    <v-text-field
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      v-model="diagnostic.valueBioHt"
    ></v-text-field>

    <p class="body-2 mb-1 mt-4">...en autres produits de qualité et durables (hors bio)</p>
    <v-text-field
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      v-model="diagnostic.valueSustainableHt"
    ></v-text-field>

    <p class="body-2 mb-1 mt-4">...en produits issus du commerce équitable</p>
    <v-text-field
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      v-model="diagnostic.valueFairTradeHt"
    ></v-text-field>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  props: {
    label: String,
    originalDiagnostic: Object,
  },
  data() {
    return {
      diagnostic: this.originalDiagnostic,
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
}
</script>
