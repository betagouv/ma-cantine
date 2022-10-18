<template>
  <v-card color="primary lighten-4" elevation="1" shaped class="d-flex align-center">
    <div class="ma-4 ml-8" v-if="$vuetify.breakpoint.smAndUp">
      <v-img max-width="100" contain src="/static/images/sitting-person-color.png"></v-img>
    </div>
    <div>
      <v-card-title class="text-body-1 font-weight-bold">
        PROLONGATION : vous avez jusqu'au 25 novembre 2022 pour participer à la collecte de données !
      </v-card-title>
      <v-card-text class="pb-0">
        Dans votre espace cantine, remplissez votre diagnostic 2021 et télédéclarez vos données (arrêté ministériel du
        14 septembre 2022). L'objectif : établir un bilan de suivi des mesures EGAlim permettant de mieux piloter cette
        politique publique par l'administration.
      </v-card-text>
      <v-card-actions>
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
