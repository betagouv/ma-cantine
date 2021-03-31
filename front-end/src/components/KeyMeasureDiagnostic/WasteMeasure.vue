<template>
  <BaseCheckbox
    v-model="diagnostic.hasMadeWasteDiagnostic"
    :label="'J’ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire'"
    :inputId="'diagnostic-made'"
  />

  <BaseCheckbox
    v-model="diagnostic.hasMadeWastePlan"
    :label="'J’ai mis en place un plan d’actions adapté au diagnostic réalisé'"
    :inputId="'plan-made'"
  />

  <BaseCheckboxes
    v-model="diagnostic.wasteActions"
    :legend="'J\'ai réalisé des actions de lutte contre le gaspillage alimentaire :'"
    :options="[
      { inputId: 'pre-registration', value: 'preRegistration', label: 'Pré-inscription des convives obligatoire' },
      { inputId: 'raise-awareness', value: 'raiseAwareness', label: 'Sensibilisation par affichage ou autre média' },
      { inputId: 'training', value: 'training', label: 'Formation / information du personnel de restauration' },
      { inputId: 'reorganization', value: 'reorganization', label: 'Réorganisation de la distribution des composantes du repas' },
      { inputId: 'portion-size', value: 'portionSize', label: 'Choix des portions (grande faim, petite faim)' },
      { inputId: 'reuse', value: 'reuse', label: 'Réutilisation des restes de préparation / surplus' },
    ]"
  />

  <BaseCheckbox
    v-model="diagnostic.hasCovenant"
    :label="'J’ai proposé des conventions de dons à des associations habilitées d’aide alimentaire'"
    :inputId="'has-covenant'"
  />
</template>

<script>
  import BaseCheckboxes from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckboxes';
  import BaseCheckbox from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckbox';

  export default {
    components: {
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
