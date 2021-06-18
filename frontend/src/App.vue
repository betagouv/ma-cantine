<template>
  <div id="app">
    <v-app>
      <Header />

      <v-main style="width: 100%">
        <v-container fluid :fill-height="!initialDataLoaded">
          <v-progress-circular
            indeterminate
            style="position: absolute; left: 50%; top: 50%"
            v-if="!initialDataLoaded"
          ></v-progress-circular>
          <router-view v-else class="mx-auto constrained" />
        </v-container>
      </v-main>

      <Footer />
      <NotificationSnackbar />
    </v-app>
  </div>
</template>

<script>
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import NotificationSnackbar from "@/components/NotificationSnackbar"

export default {
  components: {
    Header,
    Footer,
    NotificationSnackbar,
  },
  computed: {
    initialDataLoaded() {
      return this.$store.state.initialDataLoaded
    },
  },
  watch: {
    $route(to) {
      const suffix = "ma-cantine.beta.gouv.fr"
      document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
    },
    initialDataLoaded() {
      if (!this.$store.state.loggedUser) return

      const hasDiagnostics = this.$store.state.userCanteens.some((x) => x.diagnostics && x.diagnostics.length > 0)
      if (hasDiagnostics) {
        this.$store.dispatch("removeLocalStorageDiagnostics")
        return
      }

      const localStorageDiagnostics = this.$store.getters.getLocalDiagnostics()
      const canteenId = this.$store.state.userCanteens[0].id
      Promise.all(
        localStorageDiagnostics.map((payload) => this.$store.dispatch("createDiagnostic", { canteenId, payload }))
      )
        .then(() => this.$store.dispatch("removeLocalStorageDiagnostics"))
        .catch((error) => console.error(error.message))
    },
  },
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

.constrained {
  max-width: 1024px !important;
}
</style>
