<template>
  <v-sheet
    min-height="240"
    class="dsfr d-flex flex-column align-center justify-center fill-height"
    outlined
    :ripple="false"
    color="primary lighten-5"
  >
    <v-card-text class="font-weight-medium pt-0 text-center">
      <div class="mb-2">Vous êtes un acteur d'accompagnement dans la restauration collective ?</div>
      <div>Contribuez à notre initiative de référencement !</div>
    </v-card-text>
    <v-btn
      class="mt-2"
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
