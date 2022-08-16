<template>
  <v-card color="primary lighten-4" elevation="1" shaped class="d-flex align-center">
    <div class="ma-4 ml-8" v-if="$vuetify.breakpoint.smAndUp">
      <v-img max-width="100" contain src="/static/images/sitting-person-color.png"></v-img>
    </div>
    <div>
      <v-card-title class="text-body-1 font-weight-bold">Participez à la collecte de données 2022 !</v-card-title>
      <v-card-text class="pb-0">
        Du 18 juillet au 16 octobre 2022, dans votre espace diagnostic, télédéclarez vos données 2021 et devenez membre
        de la campagne nationale de télédéclaration. L'objectif : un bilan qui permettra à l'administration d'imaginer
        des services en cohérence avec la réalité du terrain. Il n'y a rien d'obligatoire, c'est du déclaratif !
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
