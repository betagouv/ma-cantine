<template>
  <v-dialog max-width="1150px" v-model="dialogOpen">
    <v-card class="text-left">
      <v-card-title class="text-h5 font-weight-black pt-6">
        Découvrez les fonctionnalités de ma cantine
      </v-card-title>
      <div class="my-6 d-none d-sm-flex justify-space-around features">
        <v-img max-width="30%" src="/static/images/features/fonctionnalite-gestion.png"></v-img>
        <v-img max-width="30%" src="/static/images/features/fonctionnalite-achats.png"></v-img>
        <v-img max-width="30%" src="/static/images/features/fonctionnalite-gestionnaires.png"></v-img>
      </div>
      <div>
        <v-card-text class="body-1 px-6">
          Gérez vos achats, suivez votre approvisionnement, publiez vos données, et plus encore !
          <br />
          Pour profiter de ces outils créez un compte ou connectez-vous.
        </v-card-text>
      </div>
      <v-divider></v-divider>
      <v-card-actions class="py-4 px-6">
        <v-spacer></v-spacer>
        <v-btn href="/s-identifier" color="primary" large outlined>M'identifier</v-btn>
        <v-btn href="/creer-mon-compte" color="primary" large>Créer mon compte</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "AuthDialog",
  props: ["value"],
  computed: {
    dialogOpen: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
  },
}
</script>

<style scoped>
.features .v-image {
  box-shadow: 1px 3px 13px -5px #1c1b1b82;
  border-radius: 5px;
}
</style>
