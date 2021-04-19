<template>
  <BaseCheckbox
    v-model="diagnostic.hasMadeWasteDiagnostic"
    label="J'ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire"
    inputId="diagnostic-made"
  />

  <BaseCheckbox
    v-model="diagnostic.hasMadeWastePlan"
    label="J'ai mis en place un plan d’actions adapté au diagnostic réalisé"
    inputId="plan-made"
  />

  <BaseCheckboxes
    v-model="diagnostic.wasteActions"
    legend="J'ai réalisé des actions de lutte contre le gaspillage alimentaire :"
    :options="wasteActions"
  />

  <BaseCheckbox
    v-model="diagnostic.hasCovenant"
    label="J'ai proposé des conventions de dons à des associations habilitées d’aide alimentaire"
    inputId="has-covenant"
  />
</template>

<script>
  import BaseCheckboxes from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckboxes';
  import BaseCheckbox from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckbox';
  import wasteActions from '@/data/waste-actions.json';

  export default {
    components: {
      BaseCheckboxes,
      BaseCheckbox
    },
    props: {
      modelValue: Object,
    },
    data() {
      return {
        wasteActions
      };
    },
    computed: {
      diagnostic() {
        return this.modelValue;
      }
    }
  }
</script>
