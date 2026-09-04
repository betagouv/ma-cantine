<template>
  <div class="mt-n2">
    <v-row class="mt-2">
      <v-col cols="12" sm="4" md="3">
        <v-card outlined class="mt-4">
          <v-list nav class="text-left">
            <v-list-item-group>
              <v-list-item :ripple="false" :to="{ name: 'AccountEditor' }">
                <v-icon small class="mr-2">$account-circle-fill</v-icon>
                <v-list-item-title class="text-body-2 font-weight-bold">Profil</v-list-item-title>
              </v-list-item>
              <v-list-item :ripple="false" :to="{ name: 'PasswordChange' }" class="rounded-lg">
                <v-icon small class="mr-2">mdi-key</v-icon>
                <v-list-item-title class="text-body-2 font-weight-bold">Mot de passe</v-list-item-title>
              </v-list-item>
              <v-list-item :ripple="false" :to="{ name: 'AccountDeletion' }" class="rounded-lg">
                <v-icon small class="mr-2">$delete-fill</v-icon>
                <v-list-item-title class="text-body-2 font-weight-bold">Supprimer mon compte</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>
      </v-col>
      <v-col>
        <router-view :key="$route.fullPath"></router-view>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "AccountSummaryPage",
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>

<style scoped>
/* for pages with left hand navigation we can make the width bigger */
.constrained {
  max-width: 1200px !important;
}
</style>
