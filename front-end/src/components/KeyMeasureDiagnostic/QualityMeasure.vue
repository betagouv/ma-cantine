<template>
  <div>
    <fieldset>
      <legend>En 2019, la valeur (en HT) de mes achats alimentaires...</legend>
      <BaseInput
        v-model="previousDiagnostic.valueTotal"
        label="...totale"
        inputId="value-total-2019"
        type="number"
        min=0
      />

      <BaseInput
        v-model="previousDiagnostic.valueBio"
        label="...de produits bio"
        inputId="value-bio-2019"
        type="number"
        min=0
      />

      <BaseInput
        v-model="previousDiagnostic.valueSustainable"
        label="...de produits durables (hors bio)"
        inputId="value-sustainable-2019"
        type="number"
        min=0
      />

      <BaseInput
        v-model="previousDiagnostic.valueFairTrade"
        label="...de produits issus du commerce équitable"
        inputId="value-fair-trade-2019"
        type="number"
        min=0
      />
    </fieldset>

    <fieldset>
      <legend>En 2020, la valeur (en HT) de mes achats alimentaires...</legend>
      <BaseInput
        v-model="latestDiagnostic.valueTotal"
        label="...totale"
        inputId="value-total-2020"
        type="number"
        min=0
      />

      <BaseInput
        v-model="latestDiagnostic.valueBio"
        label="...de produits bio"
        inputId="value-bio-2020"
        type="number"
        min=0
      />

      <BaseInput
        v-model="latestDiagnostic.valueSustainable"
        label="...de produits durables (hors bio)"
        inputId="value-sustainable-2020"
        type="number"
        min=0
      />

      <BaseInput
        v-model="latestDiagnostic.valueFairTrade"
        label="...de produits issus du commerce équitable"
        inputId="value-fair-trade-2020"
        type="number"
        min=0
      />
    </fieldset>
  </div>
</template>

<script>
  import BaseInput from '@/components/KeyMeasureDiagnostic/Inputs/BaseInput';

  export default {
    components: {
      BaseInput
    },
    props: {
      modelValue: Object,
    },
    data() {
      return {
        latestDiagnostic: this.modelValue.latest,
        previousDiagnostic: this.modelValue.previous
      }
    }
  }
</script>

<style scoped>
  div {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
  }

  fieldset {
    border: none;
    padding: 0;
    margin: 10px;
  }

  legend {
    text-align: left;
    font-weight: bold;
    padding: 0;
  }

  :deep(label) {
    font-weight: normal !important;
  }
</style>