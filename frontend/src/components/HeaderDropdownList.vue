<template>
  <v-list rounded class="text-left">
    <v-list-item-group active-class="menu-item--active">
      <v-list-item v-if="loggedUser" :ripple="false" :to="{ name: 'AccountSummaryPage' }">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-account</v-icon>
          Mon compte
        </v-list-item-title>
      </v-list-item>
      <v-list-item v-if="!loggedUser && $vuetify.breakpoint.xs" :ripple="false" href="/s-identifier">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-key</v-icon>
          S'identifier
        </v-list-item-title>
      </v-list-item>
      <v-list-item v-if="!loggedUser && $vuetify.breakpoint.xs" :ripple="false" href="/creer-mon-compte">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-account</v-icon>
          Créer un compte
        </v-list-item-title>
      </v-list-item>
      <v-divider class="mb-2" v-if="loggedUser || $vuetify.breakpoint.xs"></v-divider>
      <v-list-item v-if="$vuetify.breakpoint.xs" :ripple="false">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-hammer-wrench</v-icon>
          Devenir testeur
        </v-list-item-title>
      </v-list-item>
      <v-list-item v-if="loggedUser" :ripple="false" :to="{ name: 'CanteenInfo' }">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-publish</v-icon>
          Publier
        </v-list-item-title>
      </v-list-item>
      <v-list-item :ripple="false" :to="{ name: 'DiagnosticPage' }">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-chart-pie</v-icon>
          Autodiagnostic
        </v-list-item-title>
      </v-list-item>
      <v-divider class="mb-2"></v-divider>
      <v-list-item :ripple="false" :to="{ name: 'CanteensPage' }">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-silverware-fork-knife</v-icon>
          Nos cantines
        </v-list-item-title>
      </v-list-item>
      <v-list-item :ripple="false" :to="{ name: 'BlogsPage' }">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-newspaper-variant-outline</v-icon>
          Blog
        </v-list-item-title>
      </v-list-item>
      <v-list-item :ripple="false" href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/" target="_blank">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-file-document-outline</v-icon>
          Documentation
        </v-list-item-title>
      </v-list-item>
      <v-list-item :ripple="false" :to="{ name: 'GeneratePosterPage' }">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-text-box-check</v-icon>
          Générer mon affiche
        </v-list-item-title>
      </v-list-item>
      <v-divider class="mb-2"></v-divider>
      <v-list-item :ripple="false" href="mailto:contact@egalim.beta.gouv.fr" target="_blank">
        <v-list-item-title class="body-2">
          <v-icon small color="grey darken-2" class="mt-n1 mr-2">mdi-check</v-icon>
          Donner son avis
        </v-list-item-title>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
export default {
  name: "HeaderDropdownList",
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>

<style scoped>
.v-list--rounded .v-list-item,
.v-list--rounded .v-list-item::before,
.v-list--rounded .v-list-item > .v-ripple__container {
  border-radius: 12px !important;
}
</style>
