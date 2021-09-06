<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.cookingPlasticSubstituted"
      label="Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique"
      :readonly="readonly"
      :disabled="readonly"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.servingPlasticSubstituted"
      label="Je n’utilise plus de contenants alimentaires de service en plastique"
      :readonly="readonly"
      :disabled="readonly"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.plasticBottlesSubstituted"
      label="Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique"
      :readonly="readonly"
      :disabled="readonly"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.plasticTablewareSubstituted"
      label="Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique"
      :readonly="readonly"
      :disabled="readonly"
    />
  </div>
</template>

<script>
export default {
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
