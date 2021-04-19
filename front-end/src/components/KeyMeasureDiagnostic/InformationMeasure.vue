<template>
  <BaseCheckboxes
    v-model="diagnostic.communicationSupport"
    legend="Information sur la qualité des approvisionnements :"
    :options="communicationSupports"
  />

  <BaseInput
    v-model="diagnostic.communicationSupportLink"
    label="Lien vers le support de communication"
    inputId="communication-link"
    type="text"
  />

  <BaseCheckbox
    v-model="diagnostic.communicateOnFoodPlan"
    label="Je communique sur la mise en place d'un plan alimentaire"
    inputId="food-plan"
  />
</template>

<script>
  import BaseInput from '@/components/KeyMeasureDiagnostic/Inputs/BaseInput';
  import BaseCheckboxes from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckboxes';
  import BaseCheckbox from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckbox';
  import communicationSupports from '@/data/communication-supports.json';

  export default {
    components: {
      BaseInput,
      BaseCheckboxes,
      BaseCheckbox
    },
    props: {
      modelValue: Object,
    },
    data() {
      return {
        communicationSupports
      }
    },
    computed: {
      diagnostic() {
        return this.modelValue;
      }
    }
  }
</script>
