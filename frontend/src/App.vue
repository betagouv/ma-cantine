<template>
  <div id="app">
    <v-app>
      <AppHeader />

      <v-main style="width: 100%" class="mb-10">
        <v-banner two-line color="primary lighten-5 mb-2" mobile-breakpoint="xs">
          <div class="mx-auto constrained text-left pt-1 d-flex d-sm-block">
            <v-btn icon class="mr-1 mt-n1">
              <v-icon icon="mdi-close-circle-outline" color="primary">
                mdi-close-circle-outline
              </v-icon>
            </v-btn>

            <span class="text-caption text-sm-subtitle-1">
              Inscrivez-vous au webinaire « Création et gestion de compte » du vendredi 20 mai 12h-13h
            </span>
            <v-btn outlined class="ml-4 mt-n1" color="primary">M'inscrire</v-btn>
          </div>
        </v-banner>
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
  mounted() {
    const urlParams = new URLSearchParams(window.location.search)
    const clearCookies = Constants.TrackingParams.some((x) => !!urlParams.get(x))

    for (let i = 0; i < Constants.TrackingParams.length; i++) {
      const trackingParam = Constants.TrackingParams[i]
      const value = urlParams.get(trackingParam)

      if (clearCookies) document.cookie = `${trackingParam}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/`
      if (value) document.cookie = `${trackingParam}=${value};max-age=86400;path=/`
    }
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
