<template>
  <v-card color="deep-purple lighten-4" elevation="1" shaped class="d-flex" max-width="750">
    <div class="ma-4 ml-8 align-center">
      <v-img max-width="100" contain src="/static/images/sitting-person-color.png"></v-img>
    </div>
    <div>
      <v-card-title class="text-body-1 font-weight-bold">Participez à la campagne de télédéclaration 2022</v-card-title>
      <v-card-text>
        Du 18 juillet au 15 octobre, remplissez vos données d'appro pour l'année civile 2021 et compléter ainsi la
        collecte de données nationale.
      </v-card-text>
      <v-card-actions>
        <v-btn text>
          <v-icon class="mr-2">mdi-arrow-right</v-icon>
          En savoir plus
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
