<template>
  <CheckboxUnique
    v-model="diagnostic.cookingFoodContainersSubstituted"
    :label="'Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique'"
    :inputId="'cooking-food-container'"
  />

  <CheckboxUnique
    v-model="diagnostic.serviceFoodContainersSubstituted"
    :label="'Je n’utilise plus de contenants de service en plastique'"
    :inputId="'service-food-container'"
  />

  <CheckboxUnique
    v-model="diagnostic.waterBottlesSubstituted"
    :label="'Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique'"
    :inputId="'water-bottles'"
  />

  <CheckboxUnique
    v-model="diagnostic.disposableUstensilsSubstituted"
    :label="'Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique'"
    :inputId="'disposable-ustensils'"
  />
</template>

<script>
  import CheckboxUnique from '@/components/KeyMeasureDiagnostic/Inputs/CheckboxUnique';

  export default {
    components: {
      CheckboxUnique
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
