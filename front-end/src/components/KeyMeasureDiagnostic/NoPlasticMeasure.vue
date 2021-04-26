<template>
  <BaseCheckbox
    v-model="diagnostic.cookingFoodContainersSubstituted"
    v-if="showQuestionForSubMeasure('contenants')"
    label="Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique"
    inputId="cooking-food-container"
  />

  <BaseCheckbox
    v-model="diagnostic.serviceFoodContainersSubstituted"
    v-if="showQuestionForSubMeasure('contenants')"
    label="Je n’utilise plus de contenants de service en plastique"
    inputId="service-food-container"
  />

  <BaseCheckbox
    v-model="diagnostic.waterBottlesSubstituted"
    v-if="showQuestionForSubMeasure('bouteilles')"
    label="Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique"
    inputId="water-bottles"
  />

  <BaseCheckbox
    v-model="diagnostic.disposableUtensilsSubstituted"
    v-if="showQuestionForSubMeasure('ustensiles')"
    label="Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique"
    inputId="disposable-utensils"
  />
</template>

<script>
  import BaseCheckbox from '@/components/KeyMeasureDiagnostic/Inputs/BaseCheckbox';

  export default {
    components: {
      BaseCheckbox
    },
    props: {
      modelValue: Object,
      showQuestionForSubMeasure: Function,
    },
    computed: {
      diagnostic() {
        return this.modelValue;
      }
    }
  }
</script>
