<template>
  <BaseInput
    v-model="previousDiagnostic.valueTotal"
    label="Je connais la valeur totale (en HT) de mes achats alimentaires en 2019"
    inputId="value-total-2019"
    type="number"
    min=0
  />

  <BaseInput
    v-model="previousDiagnostic.valueBio"
    label="Je connais la valeur (en HT) des achats alimentaires de produits bio sur 2019"
    inputId="value-bio-2019"
    type="number"
    min=0
  />

  <BaseInput
    v-model="previousDiagnostic.valueSustainable"
    label="Je connais la valeur (en HT) des achats alimentaires de produits durables (hors bio) sur 2019"
    inputId="value-sustainable-2019"
    type="number"
    min=0
  />

  <BaseInput
    v-model="previousDiagnostic.valueFairTrade"
    label="Je connais la valeur (en HT) des achats alimentaires de produits issus du commerce équitable sur 2019"
    inputId="value-fair-trade-2019"
    type="number"
    min=0
  />

  <BaseInput
    v-model="latestDiagnostic.valueTotal"
    label="Je connais la valeur totale (en HT) de mes achats alimentaires en 2020"
    inputId="value-total-2020"
    type="number"
    min=0
  />

  <BaseInput
    v-model="latestDiagnostic.valueBio"
    label="Je connais la valeur (en HT) des achats alimentaires de produits bio sur 2020"
    inputId="value-bio-2020"
    type="number"
    min=0
  />

  <BaseInput
    v-model="latestDiagnostic.valueSustainable"
    label="Je connais la valeur (en HT) des achats alimentaires de produits durables (hors bio) sur 2020"
    inputId="value-sustainable-2020"
    type="number"
    min=0
  />

  <BaseInput
    v-model="latestDiagnostic.valueFairTrade"
    label="Je connais la valeur (en HT) des achats alimentaires de produits issus du commerce équitable sur 2020"
    inputId="value-fair-trade-2020"
    type="number"
    min=0
  />
</template>

<script>
  import BaseInput from '@/components/KeyMeasureDiagnostic/Inputs/BaseInput';
  import { findLatestDiagnostic, findPreviousDiagnostic } from '@/data/KeyMeasures';

  export default {
    components: {
      BaseInput
    },
    props: {
      modelValue: Object,
    },
    computed: {
      latestDiagnostic() {
        return findLatestDiagnostic(this.modelValue);
      },
      previousDiagnostic() {
        return findPreviousDiagnostic(this.modelValue);
      }
    }
  }
</script>
