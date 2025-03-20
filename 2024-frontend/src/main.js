import { createApp } from "vue"
import { createPinia } from "pinia"
import "@gouvfr/dsfr/dist/core/core.main.min.css" // Le CSS minimal du DSFR
import "@gouvfr/dsfr/dist/component/component.main.min.css" // Styles de tous les composants du DSFR
import "@gouvfr/dsfr/dist/utility/utility.main.min.css" // Classes utilitaires : les composants de VueDsfr en ont besoin
import "@gouvminint/vue-dsfr/styles" // Les styles propres aux composants de VueDsfr
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque
import i18n from "./i18n.js"
import VueMatomo from "vue-matomo"

import FoodAppleIcon from "mdi-icons/FoodApple"
import OfferIcon from "mdi-icons/Offer"
import WeatherWindyIcon from "mdi-icons/WeatherWindy"
import BullhornIcon from "mdi-icons/Bullhorn"
import LeafIcon from "mdi-icons/Leaf"
import LoadingIcon from "mdi-icons/Loading"
// "This few lines of CSS will cause the icons to scale with any surrounding text, which can be helpful when you primarily style with CSS."
// https://www.npmjs.com/package/vue-material-design-icons
import "mdi-icons/styles.css"

import "./css/reset.css"
import "./css/global.css"

import App from "./App.vue"
import { router } from "./router"

const app = createApp(App)

app.use(VueDsfr)
app.use(createPinia())
app.use(router)
app.use(i18n)

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

// deciding to keep same naming convention as previously used with Vue2 and vuetify
app.component("mdi-food-apple", FoodAppleIcon)
app.component("mdi-offer", OfferIcon)
app.component("mdi-weather-windy", WeatherWindyIcon)
app.component("mdi-bullhorn", BullhornIcon)
app.component("mdi-loading", LoadingIcon)
// TODO: get the remix icon of leaf-fill
app.component("$leaf-fill", LeafIcon)

app.mount("#app")
