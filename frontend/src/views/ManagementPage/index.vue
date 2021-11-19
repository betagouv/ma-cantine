<template>
  <div class="text-left">
    <div class="mt-4">
      <p class="my-2 text-body-1 font-weight-bold">
        Bienvenue {{ loggedUser.firstName }}
        <v-btn text class="text-decoration-underline text-caption mb-1" :to="{ name: 'AccountEditor' }">
          <v-icon class="mr-1" small>mdi-pencil</v-icon>
          Modifier mon profil
        </v-btn>
      </p>
    </div>
    <div class="mt-4">
      <h1 class="my-4 text-h5 font-weight-black">Mes cantines</h1>
      <CanteensPagination />
    </div>
    <div class="my-8">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
  </div>
</template>

<script>
import CanteensPagination from "./CanteensPagination.vue"
import UserTools from "./UserTools"

export default {
  components: { CanteensPagination, UserTools },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>
