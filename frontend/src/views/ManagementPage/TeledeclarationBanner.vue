<template>
  <v-card color="primary lighten-4" elevation="1" shaped class="d-flex align-center">
    <div class="ma-4 ml-8" v-if="$vuetify.breakpoint.smAndUp">
      <v-img max-width="100" contain src="/static/images/sitting-person-color.png"></v-img>
    </div>
    <div>
      <v-card-title class="text-body-1 font-weight-bold">
        La campagne de remontée des données 2021 est à présent terminée !
      </v-card-title>
      <v-card-text class="pb-0">
        Les données recueillies par télédéclaration seront traitées de manière agrégée pour réaliser le bilan annuel qui
        sera remis au Parlement et rendu public. Vous pouvez d'ores et déjà compléter vos diagnostics achats 2022 afin
        d'anticiper la prochaine campagne qui commencera en janvier 2023 !
      </v-card-text>
      <v-card-actions class="px-4 mt-2">
        <v-btn :to="{ name: 'PendingActions' }" color="primary">Télédéclarer mes cantines</v-btn>
        <v-btn
          text
          href="https://agriculture.gouv.fr/restauration-collective-top-depart-pour-la-premiere-collecte-dinformations-concernant-les"
          target="_blank"
          rel="noopener"
          class="text-decoration-underline"
        >
          Article sur le site du ministère
          <v-icon small class="ml-2">mdi-open-in-new</v-icon>
        </v-btn>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "TeledeclarationBanner",
}
</script>

<style scoped>
.v-sheet--shaped {
  border-radius: 26px 4px !important;
}
</style>
