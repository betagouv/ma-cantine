<template>
  <v-app>
    <WidgetHeader class="ma-4 mb-0 constrained" v-if="isWidget" />
    <AppHeader class="mx-auto constrained" v-else />

    <v-main id="contenu" style="width: 100%" :class="{ 'mb-10': !isWidget }">
      <WebinaireBanner @hide="hideBanner" v-if="showWebinaireBanner" />
      <v-container fluid :fill-height="!initialDataLoaded">
        <v-progress-circular
          indeterminate
          style="position: absolute; left: 50%; top: 50%"
          v-if="!initialDataLoaded"
        ></v-progress-circular>
        <router-view v-else :class="isWidget ? 'ma-4 mt-0 constrained' : 'mx-auto constrained'" />
      </v-container>
    </v-main>

    <AppFooter v-if="!isWidget" />
    <NotificationSnackbar v-if="!isWidget" />
  </v-app>
</template>

<script>
import AppHeader from "@/components/AppHeader"
import WidgetHeader from "@/components/WidgetHeader"
import AppFooter from "@/components/AppFooter"
import WebinaireBanner from "@/components/WebinaireBanner"
import NotificationSnackbar from "@/components/NotificationSnackbar"
import Constants from "@/constants"
import { readCookie, largestId, bannerCookieName, hideCommunityEventsBanner } from "@/utils"

export default {
  components: {
    AppHeader,
    WidgetHeader,
    AppFooter,
    NotificationSnackbar,
    WebinaireBanner,
  },
  data() {
    return {
      isWidget: window.IS_WIDGET,
    }
  },
  computed: {
    initialDataLoaded() {
      return this.$store.state.initialDataLoaded
    },
    showWebinaireBanner() {
      return this.$store.state.showWebinaireBanner && !this.isWidget
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
      this.$store.dispatch("setShowWebinaireBanner", this.webinaireCookieIsOutdated())
    },
  },
  methods: {
    hideBanner() {
      const upcomingCommunityEvents = this.$store.state.upcomingCommunityEvents
      hideCommunityEventsBanner(upcomingCommunityEvents, this.$store)
    },
    webinaireCookieIsOutdated() {
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
  background-color: #cacafb;
  border-radius: 0px;
}

.theme--light.v-card > .v-card__text,
.theme--light.v-card > .v-card__subtitle {
  color: rgba(0, 0, 0, 0.87);
}

.v-card.dsfr {
  border: solid 1px #e0e0e0;
}

.v-card.dsfr:hover {
  background-color: #f6f6f6;
}

.v-expansion-panel-header__icon > .v-icon {
  font-size: 1rem;
}
</style>
