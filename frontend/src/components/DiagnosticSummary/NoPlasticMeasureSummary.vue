<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="diagnostic.cookingPlasticSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          J’utilise encore de contenants alimentaires de cuisson / de réchauffe en plastique
        </div>
      </li>

      <li v-if="diagnostic.servingPlasticSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je n’utilise plus de contenants alimentaires de service en plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          J’utilise encore de contenants alimentaires de service en plastique
        </div>
      </li>

      <li v-if="diagnostic.plasticBottlesSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je mets encore à disposition des convives des bouteilles d’eau plate en plastique
        </div>
      </li>

      <li v-if="diagnostic.plasticTablewareSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je mets encore à disposition des convives des ustensiles à usage unique en matière plastique
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "NoPlasticMeasureSummary",
  props: {
    diagnostic: {},
  },
}
</script>
