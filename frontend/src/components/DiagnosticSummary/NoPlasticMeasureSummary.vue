<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="diagnostic.cookingPlasticSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique
        </div>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.cookingPlasticSubstituted === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          J’utilise encore de contenants alimentaires de cuisson / de réchauffe en plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Avez-vous supprimé les contenants alimentaires de cuisson / de réchauffe en plastique ?
        </div>
      </li>

      <li v-if="diagnostic.servingPlasticSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je n’utilise plus de contenants alimentaires de service en plastique
        </div>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.servingPlasticSubstituted === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          J’utilise encore de contenants alimentaires de service en plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Avez-vous supprimé les contenants alimentaires de service en plastique ?
        </div>
      </li>

      <li v-if="diagnostic.plasticBottlesSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique
        </div>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.plasticBottlesSubstituted === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je mets encore à disposition des convives des bouteilles d’eau plate en plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Avez-vous supprimé les bouteilles d’eau plate en plastique ?
        </div>
      </li>

      <li v-if="diagnostic.plasticTablewareSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique
        </div>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.plasticTablewareSubstituted === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je mets encore à disposition des convives des ustensiles à usage unique en matière plastique
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Avez-vous supprimé les ustensiles à usage unique en matière plastique ?
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { diagnosticUsesNullAsFalse } from "@/utils"

export default {
  name: "NoPlasticMeasureSummary",
  props: {
    diagnostic: {},
  },
  computed: {
    diagnosticUsesNullAsFalse() {
      return diagnosticUsesNullAsFalse(this.diagnostic)
    },
  },
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding-left: 0;
}
li {
  margin-bottom: 14px;
  display: flex;
}
li .v-icon {
  align-items: baseline;
}
</style>
