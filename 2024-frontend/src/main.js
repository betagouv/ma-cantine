/* Vue chore */
import { createApp } from "vue"
import { createPinia } from "pinia"

/* DSFR */
import "@gouvfr/dsfr/dist/utility/utility.main.min.css" // Classes utilitaires
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque

/* Plugins */
import i18n from "./i18n.js"
import VueMatomo from "vue-matomo"

/* Icons */
import FoodAppleIcon from "mdi-icons/FoodApple"
import OfferIcon from "mdi-icons/Offer"
import WeatherWindyIcon from "mdi-icons/WeatherWindy"
import BullhornIcon from "mdi-icons/Bullhorn"
import LeafIcon from "mdi-icons/Leaf"
import LoadingIcon from "mdi-icons/Loading"
import DeleteIcon from "mdi-icons/Loading"
// "This few lines of CSS will cause the icons to scale with any surrounding text, which can be helpful when you primarily style with CSS."
// https://www.npmjs.com/package/vue-material-design-icons
import "mdi-icons/styles.css"

/* Global CSS custom */
import "./css/reset.css"
import "./css/global.css"

/* App */
import App from "./App.vue"
import { router } from "./router"

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

/*
  Icons reusable components
  deciding to keep same naming convention as previously used with Vue2 and vuetify
*/
app.component("mdi-food-apple", FoodAppleIcon)
app.component("mdi-offer", OfferIcon)
app.component("mdi-weather-windy", WeatherWindyIcon)
app.component("mdi-bullhorn", BullhornIcon)
app.component("mdi-loading", LoadingIcon)
app.component("mdi-delete", DeleteIcon)
// TODO: get the remix icon of leaf-fill
app.component("$leaf-fill", LeafIcon)

app.mount("#app")
