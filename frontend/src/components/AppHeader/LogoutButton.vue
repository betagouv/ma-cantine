<template>
  <v-dialog v-model="logoutWarningDialog" max-width="500">
    <template v-slot:activator="{ on, attrs }">
      <v-btn v-bind="attrs" v-on="on" text elevation="0" class="primary--text">
        <span>Me déconnecter</span>
      </v-btn>
    </template>

    <v-card>
      <v-card-text class="pa-8 text-left">
        <p class="mb-0">Voulez-vous vous déconnecter de votre compte ma cantine ?</p>
      </v-card-text>

      <v-divider aria-hidden="true" role="presentation"></v-divider>

      <v-card-actions class="flex-wrap align-end">
        <v-btn color="grey darken-2" text @click="logoutWarningDialog = false" class="mr-1">
          Non, revenir en arrière
        </v-btn>
        <v-btn color="red darken-2" text @click="logout">
          Oui, je confirme
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "LogoutButton",
  data() {
    return {
      logoutWarningDialog: false,
    }
  },
  methods: {
    logout() {
      return this.$store.dispatch("logout")
    },
  },
}
</script>

<style></style>
