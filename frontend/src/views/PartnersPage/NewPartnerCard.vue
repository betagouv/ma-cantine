<template>
  <v-sheet
    min-height="240"
    class="dsfr d-flex flex-column align-start justify-center fill-height callout pl-4"
    outlined
    :ripple="false"
    color="grey lighten-4"
  >
    <v-card-title class="font-weight-bold">
      Vous êtes un acteur d'accompagnement dans la restauration collective ?
    </v-card-title>
    <v-card-text>
      Contribuez à notre initiative de référencement !
    </v-card-text>
    <v-btn
      class="ma-4"
      color="primary"
      href="https://startupdetat.typeform.com/to/JhhsMCYC"
      target="_blank"
      rel="noopener"
    >
      Me recenser
      <v-icon small class="ml-2">mdi-open-in-new</v-icon>
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
