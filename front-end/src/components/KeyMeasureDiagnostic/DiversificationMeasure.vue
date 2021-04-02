<template>
  <BaseCheckbox
    v-model="diagnostic.hasMadeDiversificationPlan"
    label="J'ai mis en place un plan pluriannuel de diversification des protéines"
    inputId="plan-made"
  />

  <BaseRadios
    v-model="diagnostic.vegetarianFrequency"
    legend="J'ai mis en place un menu végétarien dans ma cantine :"
    :options="[
      { inputId: 'less-than-once', value: 'lessThanOnce', label: 'Moins d\'une fois par semaine' },
      { inputId: 'once', value: 'once', label: 'Une fois par semaine' },
      { inputId: 'more-than-once', value: 'moreThanOnce', label: 'Plus d\'une fois par semaine' },
    ]"
  />

  <BaseRadios
    v-model="diagnostic.vegetarianMenuType"
    legend="Le menu végétarien proposé est :"
    :options="[
      { inputId: 'standalone', value: 'standalone', label: 'Un menu végétarien unique' },
      { inputId: 'all-vegetarian', value: 'allVegetarian', label: 'Plusieurs menus végétariens alternatifs' },
      { inputId: 'alternative', value: 'alternative', label: 'Un menu végétarien alternatif à d\'autres menus non-végétariens' },
    ]"
  />
</template>

<script>
import BaseCheckbox from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckbox';
import BaseRadios from '@/components/KeyMeasureDiagnostic/Inputs/BaseRadios';

  export default {
    components: {
      BaseCheckbox,
      BaseRadios
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
