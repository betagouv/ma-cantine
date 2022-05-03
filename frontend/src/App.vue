<template>
  <div id="app">
    <v-app>
      <AppHeader />

      <v-main style="width: 100%" class="mb-10">
        <v-container fluid :fill-height="!initialDataLoaded">
          <v-progress-circular
            indeterminate
            style="position: absolute; left: 50%; top: 50%"
            v-if="!initialDataLoaded"
          ></v-progress-circular>
          <router-view v-else class="mx-auto constrained" />
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
      document.querySelector('meta[property="og:url"]').setAttribute("content", window.location)
    },
    initialDataLoaded() {
      if (!this.$store.state.loggedUser) return
      this.$store.dispatch("removeLocalStorageDiagnostics")
    },
  },
  beforeMount() {
    window.$crisp.push(["do", "chat:hide"])
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

.v-menu__content {
  text-align: left;
}
</style>
