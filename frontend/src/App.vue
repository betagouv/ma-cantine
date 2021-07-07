<template>
  <div id="app">
    <v-app>
      <AppHeader />

      <v-main style="width: 100%">
        <v-container fluid :fill-height="!initialDataLoaded">
          <v-progress-circular
            indeterminate
            style="position: absolute; left: 50%; top: 50%"
            v-if="!initialDataLoaded"
          ></v-progress-circular>
          <router-view v-else class="mx-auto constrained" :key="$route.fullPath" />
        </v-container>
      </v-main>

      <AppFooter />
      <NotificationSnackbar />
    </v-app>
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader"
import AppFooter from "@/components/AppFooter"
import NotificationSnackbar from "@/components/NotificationSnackbar"
import { getObjectDiff } from "@/utils"
import Constants from "@/constants"

export default {
  components: {
    AppHeader,
    AppFooter,
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
      if (!this.$store.state.loggedUser || !this.$store.state.userCanteens.length) return

      const hasDiagnostics = this.$store.state.userCanteens.some((x) => x.diagnostics && x.diagnostics.length > 0)
      if (hasDiagnostics) {
        this.$store.dispatch("removeLocalStorageDiagnostics")
        return
      }

      const localStorageDiagnostics = this.$store.getters.getLocalDiagnostics()
      const canteenId = this.$store.state.userCanteens[0].id
      Promise.all(
        localStorageDiagnostics.map((payload) => {
          const diagnosticChanges = getObjectDiff(Constants.DefaultDiagnostics, payload)
          const isDefaultDiagnostic = Object.keys(diagnosticChanges).length === 1 && "year" in diagnosticChanges

          if (isDefaultDiagnostic) return true
          return this.$store.dispatch("createDiagnostic", { canteenId, payload })
        })
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
