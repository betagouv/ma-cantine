<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.cookingPlasticSubstituted"
      label="Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.servingPlasticSubstituted"
      label="Je n’utilise plus de contenants de service en plastique"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.plasticBottlesSubstituted"
      label="Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.plasticTablewareSubstituted"
      label="Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique"
    />
  </div>
</template>

<script>
export default {
  props: {
    diagnostic: Object,
  },
}
</script>
