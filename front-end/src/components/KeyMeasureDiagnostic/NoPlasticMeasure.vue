<template>
  <BaseCheckbox
    v-model="diagnostic.cookingFoodContainersSubstituted"
    label="Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique"
    inputId="cooking-food-container"
  />

  <BaseCheckbox
    v-model="diagnostic.serviceFoodContainersSubstituted"
    label="Je n’utilise plus de contenants de service en plastique"
    inputId="service-food-container"
  />

  <BaseCheckbox
    v-model="diagnostic.waterBottlesSubstituted"
    label="Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique"
    inputId="water-bottles"
  />

  <BaseCheckbox
    v-model="diagnostic.disposableUtensilsSubstituted"
    label="Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique"
    inputId="disposable-utensils"
  />
</template>

<script>
  import BaseCheckbox from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckbox';
  import { findLatestDiagnostic } from '@/data/KeyMeasures';

  export default {
    components: {
      BaseCheckbox
    },
    props: {
      modelValue: Object,
    },
    computed: {
      diagnostic() {
        return findLatestDiagnostic(this.modelValue);
      }
    }
  }
</script>
