<template>
  <v-sheet
    min-height="240"
    class="dsfr d-flex flex-column align-start justify-center fill-height callout pl-4"
    outlined
    :ripple="false"
    color="grey lighten-4"
  >
    <v-card-title>
      <h2 class="fr-h5 mb-0">
        Vous êtes un acteur d'accompagnement dans la restauration collective ?
      </h2>
    </v-card-title>
    <v-card-text>
      <p class="mb-0">
        Contribuez à notre initiative de référencement !
      </p>
    </v-card-text>
    <v-btn class="ma-4 mt-2" color="primary" :to="{ name: 'NewPartner' }">
      Me recenser
    </v-btn>
  </v-sheet>
</template>

<script>
export default {
  name: "NewPartnerCard",
}
</script>

<style scoped>
.callout {
  box-shadow: rgb(106, 106, 244) 4px 0px 0px 0px inset !important;
}
</style>
