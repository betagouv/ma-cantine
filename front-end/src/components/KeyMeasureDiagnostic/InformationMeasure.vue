<template>
  <BaseCheckboxes
    v-model="diagnostic.communicationSupport"
    v-if="showQuestionForSubMeasure('convives-informes')"
    legend="Information sur la qualité des approvisionnements :"
    :options="communicationSupports"
  />

  <BaseInput
    v-model="diagnostic.communicationSupportLink"
    v-if="showQuestionForSubMeasure('convives-informes')"
    label="Lien vers le support de communication"
    inputId="communication-link"
    type="text"
  />

  <BaseCheckbox
    v-model="diagnostic.communicateOnFoodPlan"
    v-if="showQuestionForSubMeasure('informations-nutritionnelles')"
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
      showQuestionForSubMeasure: Function,
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
