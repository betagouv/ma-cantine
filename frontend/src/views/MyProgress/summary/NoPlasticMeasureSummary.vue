<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="displayDiagnostic.cookingPlasticSubstituted">
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

      <li v-if="displayDiagnostic.servingPlasticSubstituted">
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

      <li v-if="displayDiagnostic.plasticBottlesSubstituted">
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

      <li v-if="displayDiagnostic.plasticTablewareSubstituted">
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
  display: flex;
}
li .v-icon {
  align-items: baseline;
}
</style>
