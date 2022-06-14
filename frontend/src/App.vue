<template>
  <div id="app">
    <v-app>
      <AppHeader class="mx-auto constrained" />

      <v-main style="width: 100%" class="mb-10">
        <WebinaireBanner @hide="hideBanner" v-if="showWebinaireBanner" />
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
import WebinaireBanner from "@/components/WebinaireBanner"
import NotificationSnackbar from "@/components/NotificationSnackbar"
import Constants from "@/constants"
import { readCookie, largestId, bannerCookieName, hideCommunityEventsBanner } from "@/utils"

export default {
  components: {
    AppHeader,
    AppFooter,
    NotificationSnackbar,
    WebinaireBanner,
  },
  computed: {
    initialDataLoaded() {
      return this.$store.state.initialDataLoaded
    },
    showWebinaireBanner() {
      const upcomingCommunityEvents = this.$store.state.upcomingCommunityEvents
      if (upcomingCommunityEvents.length === 0) {
        return false
      }
      const lastHiddenEventId = readCookie(bannerCookieName)
      if (lastHiddenEventId) {
        const lastEventId = largestId(upcomingCommunityEvents)
        return lastEventId > parseInt(lastHiddenEventId, 10)
      } else {
        return true
      }
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
      const suffix = "ma cantine"
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
  methods: {
    hideBanner() {
      const upcomingCommunityEvents = this.$store.state.upcomingCommunityEvents
      hideCommunityEventsBanner(upcomingCommunityEvents)
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

.v-menu__content {
  text-align: left;
}

.cta-group {
  background-color: #b6d9c8;
  border-radius: 16px;
}
</style>
