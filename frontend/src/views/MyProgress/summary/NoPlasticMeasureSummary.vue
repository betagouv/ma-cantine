<template>
  <div class="fr-text">
    <ul>
      <li v-if="displayDiagnostic.cookingPlasticSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Je n’utilise plus de contenants alimentaires de cuisson / de réchauffe en plastique
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        J’utilise encore de contenants alimentaires de cuisson / de réchauffe en plastique
      </li>

      <li v-if="displayDiagnostic.servingPlasticSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Je n’utilise plus de contenants alimentaires de service en plastique
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        J’utilise encore de contenants alimentaires de service en plastique
      </li>

      <li v-if="displayDiagnostic.plasticBottlesSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Je ne mets plus à disposition des convives des bouteilles d’eau plate en plastique
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        Je mets encore à disposition des convives des bouteilles d’eau plate en plastique
      </li>

      <li v-if="displayDiagnostic.plasticTablewareSubstituted">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Je ne mets plus à disposition des convives des ustensiles à usage unique en matière plastique
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        Je mets encore à disposition des convives des ustensiles à usage unique en matière plastique
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "NoPlasticMeasureSummary",
  props: {
    diagnostic: {},
    centralDiagnostic: {},
  },
  computed: {
    usesCentralDiagnostic() {
      return this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
    displayDiagnostic() {
      return this.usesCentralDiagnostic ? this.centralDiagnostic : this.diagnostic
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
}
</style>
