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
      return this.$store.state.showWebinaireBanner
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

/* Icons */
span.icon,
span.icon::before {
  /* override these two variables to change the size of the icon and it's alignment relative to text */
  --icon-size: 1.75rem;
  --font-size: 2rem;
  vertical-align: calc(var(--font-size) - var(--icon-size) * 0.95);
  height: var(--icon-size);
  width: var(--icon-size);
  overflow: hidden; /* text can be added in the span, only visible to screen readers and with css disabled */
  display: inline-block;
}
span.icon::before {
  content: "";
  flex: 0 0 auto;
  --blue-france-sun-113-625: #000091;
  background-color: var(--blue-france-sun-113-625);
  -webkit-mask-image: var(--icon-image);
  mask-image: var(--icon-image);
}
span.i-arrow-right::before {
  --icon-image: url("/static/icons/arrow-right-line.svg");
}
span.i-restaurant::before {
  --icon-image: url("/static/icons/restaurant-fill.svg");
}
span.i-team::before {
  --icon-image: url("/static/icons/team-fill.svg");
}
span.i-leaf::before {
  --icon-image: url("/static/icons/leaf-fill.svg");
  background-color: #43a047; /* Vuetify green darken-2 */
}
span.mdi-food-apple::before {
  --icon-image: url("/static/icons/mdi-food-apple.svg");
  background-color: #f44336; /* Vuetify red */
}
span.mdi-bullhorn::before {
  --icon-image: url("/static/icons/mdi-bullhorn.svg");
  background-color: #ffa000; /* Vuetify amber darken-2 */
}
span.mdi-offer::before {
  --icon-image: url("/static/icons/mdi-offer.svg");
  background-color: #f57c00; /* Vuetify orange darken-2 */
}
span.mdi-weather-windy::before {
  --icon-image: url("/static/icons/mdi-weather-windy.svg");
  background-color: #1e88e5; /* Vuetify blue darken-1 */
}
</style>
