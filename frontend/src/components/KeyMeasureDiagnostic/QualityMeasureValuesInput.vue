<template>
  <fieldset class="d-flex flex-column">
    <!-- TODO: Use text field suffix (euros HT) instead of (en HT) here? -->
    <legend class="my-2">{{ label }}</legend>

    <label :for="'total-' + diagnostic.year" class="body-2 mb-1 mt-2">...totale</label>
    <v-text-field
      :id="'total-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[
        validators.nonNegativeOrEmpty,
        validators.gteSum(
          [diagnostic.valueBioHt, diagnostic.valueSustainableHt, diagnostic.valueFairTradeHt, diagnostic.valuePatHt],
          totalErrorMessage
        ),
      ]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :messages="totalError ? [totalErrorMessage] : undefined"
      :error="totalError"
      @blur="totalError = false"
    ></v-text-field>

    <label :for="'bio-' + diagnostic.year" class="body-2 mb-1 mt-4">...en produits bio</label>
    <v-text-field
      :id="'bio-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      v-model.number="diagnostic.valueBioHt"
      :readonly="readonly"
      :disabled="readonly"
      @blur="checkTotal"
    ></v-text-field>

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
      v-model.number="diagnostic.valueSustainableHt"
      :readonly="readonly"
      :disabled="readonly"
      @blur="checkTotal"
    ></v-text-field>

    <label :for="'fairtrade-' + diagnostic.year" class="body-2 mb-1 mt-4">
      ...en produits issus du commerce équitable
    </label>
    <v-text-field
      :id="'fairtrade-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      v-model.number="diagnostic.valueFairTradeHt"
      :readonly="readonly"
      :disabled="readonly"
      @blur="checkTotal"
    ></v-text-field>

    <div v-if="includePat" class="mb-1 mt-4">
      <label :for="'pat-' + diagnostic.year" class="body-2">
        ...en produits dans le cadre de Projects Alimentaires Territoriaux
      </label>
      <v-text-field
        :id="'pat-' + diagnostic.year"
        hide-details="auto"
        type="number"
        :rules="[validators.nonNegativeOrEmpty]"
        validate-on-blur
        solo
        placeholder="Je ne sais pas"
        v-model.number="diagnostic.valuePatHt"
        :readonly="readonly"
        :disabled="readonly"
        @blur="checkTotal"
      ></v-text-field>
    </div>
  </fieldset>
</template>

<script>
import validators from "@/validators"

export default {
  props: {
    label: String,
    originalDiagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
    includePat: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      diagnostic: this.originalDiagnostic,
      totalError: false,
      totalErrorMessage: "Le totale ne peut pas être moins que le somme des valeurs suivantes",
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
  methods: {
    checkTotal() {
      const result = validators.gteSum(
        [
          this.diagnostic.valueBioHt,
          this.diagnostic.valueSustainableHt,
          this.diagnostic.valueFairTradeHt,
          this.diagnostic.valuePatHt,
        ],
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
