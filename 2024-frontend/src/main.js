/* Vue chore */
import App from "./App.vue"
import { createApp } from "vue"
import { createPinia } from "pinia"
import { router } from "./router"

/* DSFR */
import "@gouvfr/dsfr/dist/utility/utility.main.min.css" // Classes utilitaires
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque

/* DSFR Chart */
import "@gouvfr/dsfr-chart"
import "@gouvfr/dsfr-chart/css"

/* Plugins */
import i18n from "./i18n.js"
import VueMatomo from "vue-matomo"

/* Global CSS custom */
import "./css/reset.css"
import "./css/global.css"

/* Create App */
const app = createApp(App)
app.use(VueDsfr)
app.use(createPinia())
app.use(router)
app.use(i18n)

/* Matomo Tracking */
if (window.MATOMO_ID) {
  app.use(VueMatomo, {
    host: "https://stats.beta.gouv.fr",
    siteId: window.MATOMO_ID,
    trackerFileName: "matomo",
    router: router,
    requireConsent: false,
    enableLinkTracking: true,
    trackInitialView: false,
    debug: false,
    userId: undefined,
  })
}

app.mount("#app")
