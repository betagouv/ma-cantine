<template>
  <v-card elevation="0" class="text-left">
    <v-card-title>
      <h1 class="font-weight-black text-h4 mb-4 mt-1">Supprimer mon compte</h1>
    </v-card-title>
    <v-card-subtitle class="text-body-2 mt-n1">
      Contactez nous pour supprimer votre compte ou demander les données liées à votre profil
    </v-card-subtitle>
    <v-card-actions class="pa-4">
      <v-btn large outlined color="primary" :href="hrefMail" target="_blank">Contacter l'équipe</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "AccountDeletion",
  computed: {
    hrefMail() {
      const loggedUser = this.$store.state.loggedUser
      return `mailto:support-egalim@beta.gouv.fr?subject=Suppression de mon compte : ${loggedUser.email}`
    },
  },
}
</script>
