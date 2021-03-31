<template>
  <BasicInput
    v-model="diagnostic['2019'].valueTotal"
    :label="'Je connais la valeur totale (en HT) de mes achats alimentaires en 2019'"
    :inputId="'value-total-2019'"
    :type="'number'"
    :min="0"
  />

  <BasicInput
    v-model="diagnostic['2019'].valueBio"
    :label="'Je connais la valeur (en HT) des achats alimentaires de produits bio sur 2019'"
    :inputId="'value-bio-2019'"
    :type="'number'"
    :min="0"
  />

  <BasicInput
    v-model="diagnostic['2019'].valueSustainable"
    :label="'Je connais la valeur (en HT) des achats alimentaires de produits durables (hors bio) sur 2019'"
    :inputId="'value-sustainable-2019'"
    :type="'number'"
    :min="0"
  />

  <BasicInput
    v-model="diagnostic['2019'].valueFairTrade"
    :label="'Je connais la valeur (en HT) des achats alimentaires de produits issus du commerce équitable sur 2019'"
    :inputId="'value-fair-trade-2019'"
    :type="'number'"
    :min="0"
  />

  <BasicInput
    v-model="diagnostic['2020'].valueTotal"
    :label="'Je connais la valeur totale (en HT) de mes achats alimentaires en 2020'"
    :inputId="'value-total-2020'"
    :type="'number'"
    :min="0"
  />

  <BasicInput
    v-model="diagnostic['2020'].valueBio"
    :label="'Je connais la valeur (en HT) des achats alimentaires de produits bio sur 2020'"
    :inputId="'value-bio-2020'"
    :type="'number'"
    :min="0"
  />

  <BasicInput
    v-model="diagnostic['2020'].valueSustainable"
    :label="'Je connais la valeur (en HT) des achats alimentaires de produits durables (hors bio) sur 2020'"
    :inputId="'value-sustainable-2020'"
    :type="'number'"
    :min="0"
  />

  <BasicInput
    v-model="diagnostic['2020'].valueFairTrade"
    :label="'Je connais la valeur (en HT) des achats alimentaires de produits issus du commerce équitable sur 2020'"
    :inputId="'value-fair-trade-2020'"
    :type="'number'"
    :min="0"
  />
</template>

<script>
  import BasicInput from '@/components/KeyMeasureDiagnostic/Inputs/BasicInput';

  export default {
    components: {
      BasicInput
    },
    props: {
      modelValue: Object,
    },
    computed: {
      diagnostic() {
        return this.modelValue;
      }
    }
  }
</script>
