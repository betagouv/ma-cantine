<template>
  <v-app>
    <WidgetHeader class="ma-4 mb-0 constrained" v-if="isWidget" />
    <AppHeader class="mx-auto constrained" v-else-if="!fullscreen" />

    <v-main id="contenu" style="width: 100%" :class="{ 'mb-10': !isWidget, 'fill-height': fullscreen }" role="main">
      <AppBanner v-if="!isWidget && !fullscreen" />
      <AppBannerAlert v-if="!isWidget && !fullscreen" />
      <WebinaireBanner @hide="hideBanner" v-if="showWebinaireBanner && !fullscreen" />
      <v-container fluid :fill-height="!initialDataLoaded || fullscreen" :class="{ 'pa-0': fullscreen }">
        <v-progress-circular
          indeterminate
          style="position: absolute; left: 50%; top: 50%"
          v-if="!initialDataLoaded"
        ></v-progress-circular>
        <router-view v-else :class="routerViewClass" />
      </v-container>
    </v-main>

    <AppFooter v-if="!isWidget && !fullscreen" />
    <div v-if="!isWidget" id="notification-center">
      <NotificationSnackbar v-for="notification in notifications" :key="notification.id" :notification="notification" />
    </div>
  </v-app>
</template>

<script>
import AppHeader from "@/components/AppHeader"
import AppBanner from "@/components/AppBanner"
import AppBannerAlert from "@/components/AppBannerAlert"
import WidgetHeader from "@/components/WidgetHeader"
import AppFooter from "@/components/AppFooter"
import WebinaireBanner from "@/components/WebinaireBanner"
import NotificationSnackbar from "@/components/NotificationSnackbar"
import Constants from "@/constants"
import { readCookie, largestId, bannerCookieName, hideCommunityEventsBanner } from "@/utils"

export default {
  components: {
    AppHeader,
    AppBanner,
    AppBannerAlert,
    WidgetHeader,
    AppFooter,
    NotificationSnackbar,
    WebinaireBanner,
  },
  data() {
    return {
      isWidget: window.IS_WIDGET,
      fullscreen: false,
    }
  },
  computed: {
    initialDataLoaded() {
      return this.$store.state.initialDataLoaded
    },
    showWebinaireBanner() {
      return this.$store.state.showWebinaireBanner && !this.isWidget
    },
    routerViewClass() {
      if (this.isWidget) return "ma-4 mt-0 constrained"
      if (this.fullscreen) return ""
      return "mx-auto constrained"
    },
    notifications() {
      return this.$store.state.notifications
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
      this.fullscreen = this.$route.meta.fullscreen
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

<style lang="scss">
@import "scss/dsfr.scss";

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

.v-card.dsfr.no-hover:hover {
  background-color: inherit;
}

// thanks to https://codesandbox.io/p/sandbox/awesome-clickable-card-8tgtwt?file=%2Fstyle.css%3A16%2C1-19%2C2
// makes link titles much less verbose for improved accessible experience
.v-card.dsfr.expanded-link {
  position: relative;
  isolation: isolate;
}

.v-card.dsfr.expanded-link a {
  text-decoration: none;
}

.v-card.dsfr.expanded-link a::after {
  content: "";
  position: absolute;
  z-index: 1;

  inset: 0;
}
.v-card.dsfr.expanded-link button,
.v-card.dsfr.expanded-link a {
  z-index: 2;
}

a:focus,
button:focus,
.v-input--checkbox:focus-within,
.v-radio:focus-within,
.v-card:focus,
.drag-and-drop:focus-within,
div[role="tab"]:focus,
.outline-focus-within:focus-within {
  outline: rgb(0, 0, 145) !important;
  outline-width: 1px !important;
  outline-style: auto !important;
  outline-offset: 2px;
}

.v-btn.primary:hover {
  background-color: #1212ff !important;
}

.v-expansion-panel-header__icon > .v-icon {
  font-size: 1rem;
}

.theme--light.v-btn.v-btn--disabled {
  color: #757575 !important; // grey--text text--darken-1 for a11y
}
.theme--light.v-input input::placeholder,
.theme--light.v-input textarea::placeholder {
  color: #666 !important;
  opacity: 1;
  font-style: italic;
}
.other-text-input label.theme--light.v-label--is-disabled {
  color: #666 !important;
  opacity: 1;
}

.dsfr-table.theme--light.v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  color: #000091;
}
.dsfr-table.grey--table.theme--light.v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  color: #3a3a3a;
}
.dsfr-table.v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  height: 32px;
}
.dsfr-table.theme--light.v-data-table > .v-data-table__wrapper > table > thead > tr:last-child > th {
  border-bottom: thin solid #000091;
}
.dsfr-table.grey--table.theme--light.v-data-table > .v-data-table__wrapper > table > thead > tr:last-child > th {
  border-bottom: thin solid #3a3a3a;
}
.dsfr-table.v-data-table > .v-data-table__wrapper > table > tbody > tr.v-data-table__empty-wrapper > td {
  padding: 0px;
}
// no IE8 support
.dsfr-table > .v-data-table__wrapper > table > tbody > tr:nth-child(even) {
  background-color: #f5f5f5;
}
.dsfr-table.grey--table > .v-data-table__wrapper > table > tbody > tr:nth-child(even) {
  background-color: #f6f6f6;
}
.dsfr-table.theme--light.v-data-table
  > .v-data-table__wrapper
  > table
  > tbody
  > tr:not(:last-child)
  > td:not(.v-data-table__mobile-row) {
  border-bottom: none;
}
.dsfr-table.theme--light.v-data-table > .v-data-table__wrapper > table > tbody > tr:not(.v-data-table__empty-wrapper) {
  pointer-events: none; // disable background colour change on hover
}
.dsfr-table.table-preview > .v-data-table__wrapper > table > tbody > tr:nth-child(3) {
  // Not supported by all browsers, but is a nice to have rather than necessity
  -webkit-mask-image: -webkit-gradient(linear, left top, left bottom, from(rgba(0, 0, 0, 0.6)), to(rgba(0, 0, 0, 0)));
}
.fr-btn--tertiary {
  border: thin solid #ddd;
}
fieldset {
  border: none;
}
ul.no-bullets,
ol.no-bullets {
  padding-left: 0;
  list-style-type: none;
  /* https://developer.mozilla.org/en-US/docs/Web/CSS/list-style-type#accessibility_concerns */
  li::before {
    content: "\200B";
  }
}
.dark-orange {
  color: #d64309 !important; // 4.5:1 contrast for text on white
}
#notification-center {
  position: fixed;
  z-index: 1000;
  height: fit-content;
  right: 0;

  .v-snack__wrapper {
    margin: 2px;
    min-width: unset;
  }
}
</style>
