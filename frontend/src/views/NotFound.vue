<template>
  <v-card elevation="0" class="text-left">
    <v-card-title class="text-h2 font-weight-black my-8">
      Oups !
    </v-card-title>
    <v-card-subtitle class="text-h6 grey--text text--darken-4">
      La page que vous recherchez semble introuvable
    </v-card-subtitle>
    <v-card-text v-if="!isWidget">
      <v-btn x-large color="primary" class="mt-4" :to="{ name: 'LandingPage' }">Revenir à l'accueil</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return { isWidget: window.IS_WIDGET }
  },
}
</script>
