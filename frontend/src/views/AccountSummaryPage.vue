<template>
  <div>
    <v-card elevation="0" class="mt-2">
      <v-card-text>
        <v-avatar color="grey lighten-3" size="100">
          <v-img v-if="loggedUser.avatar" :src="loggedUser.avatar"></v-img>
          <v-icon large v-else>mdi-account</v-icon>
        </v-avatar>
      </v-card-text>

      <v-card-title class="d-block text-h4 font-weight-black text-center mb-2">
        {{ loggedUser.firstName }} {{ loggedUser.lastName }}
      </v-card-title>
      <v-card-subtitle>
        <div>
          <v-icon class="mt-n1 mr-2" small>mdi-account</v-icon>
          {{ loggedUser.username }}
        </div>
        <div>
          <v-icon class="mt-n1 mr-2" small>mdi-email</v-icon>
          {{ loggedUser.email }}
        </div>
      </v-card-subtitle>
      <v-card-text class="mt-4 mb-n2">
        <v-btn large color="primary" :to="{ name: 'ManagementPage' }">Gérer mes cantines</v-btn>
      </v-card-text>
      <v-card-text class="mt-14">
        <v-btn color="red" text class="text-decoration-underline" href="/se-deconnecter">
          <v-icon small class="mr-2">mdi-exit-to-app</v-icon>
          Me déconnecter
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>
