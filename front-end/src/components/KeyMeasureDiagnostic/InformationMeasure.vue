<template>
  <BaseCheckboxes
    v-model="diagnostic.communicationSupport"
    legend="Information sur la qualité des approvisionnements :"
    :options="[
      { inputId: 'email-communication', value: 'email', label: 'Envoi d\'e-mail aux convives ou à leurs représentants' },
      { inputId: 'display-communication', value: 'display', label: 'Par affichage sur le lieu de restauration' },
      { inputId: 'website-communication', value: 'website', label: 'Sur site internet ou intranet (mairie, cantine)' },
      { inputId: 'other-communication', value: 'other', label: 'Autres moyens d\'affichage et de communication électronique' },
    ]"
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

  export default {
    components: {
      BaseInput,
      BaseCheckboxes,
      BaseCheckbox
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
