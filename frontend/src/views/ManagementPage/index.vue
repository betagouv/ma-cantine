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
      <CanteensPagination :canteens="canteens" />
    </div>
    <div class="my-12">
      <h2 class="mb-4 text-h5 font-weight-black">Mes diagnostics</h2>
      <DiagnosticIntroduction v-if="!hasDiagnostics" class="body-2"></DiagnosticIntroduction>
      <div class="mb-8 ml-n4">
        <v-btn text color="primary" :to="{ name: 'NewDiagnostic' }" v-if="canteens.length">
          <v-icon class="mr-2">mdi-plus</v-icon>
          Ajouter un diagnostic
        </v-btn>
      </div>

      <DiagnosticsPagination :canteens="canteens" />
    </div>
    <div class="my-8">
      <h2 class="text-h5 font-weight-black mb-4">Mes outils</h2>
      <UserTools />
    </div>
  </div>
</template>

<script>
import CanteensPagination from "./CanteensPagination.vue"
import DiagnosticsPagination from "./DiagnosticsPagination"
import DiagnosticIntroduction from "@/components/DiagnosticIntroduction"
import UserTools from "./UserTools"

export default {
  components: { CanteensPagination, DiagnosticsPagination, DiagnosticIntroduction, UserTools },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    canteens() {
      return [...this.$store.state.userCanteens].sort((a, b) => (a.name > b.name ? 1 : -1))
    },
    hasDiagnostics() {
      return this.canteens.length && this.canteens.some((c) => !!c.diagnostics.length)
    },
  },
}
</script>
