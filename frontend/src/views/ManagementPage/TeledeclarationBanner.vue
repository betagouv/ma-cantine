<template>
  <v-card color="primary lighten-4" elevation="1" shaped class="d-flex align-center">
    <div>
      <v-card-title class="text-body-1 font-weight-bold">
        La campagne de remontée des données 2021 est à présent terminée !
      </v-card-title>
      <v-card-text class="pb-6">
        Les données recueillies par télédéclaration seront traitées de manière agrégée pour réaliser le bilan annuel qui
        sera remis au Parlement et rendu public. Vous pouvez d'ores et déjà compléter vos diagnostics 2022 afin
        d'anticiper la prochaine campagne qui commencera en janvier 2023 !
      </v-card-text>
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
