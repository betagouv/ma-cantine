import { createApp } from "vue"
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque

import App from "./App.vue"
import { router } from "./router"
import store from "./store"
import vuetify from "./plugins/vuetify"

createApp(App)
  .use(vuetify)
  .use(VueDsfr) // Enregistrement de la bibliothèque en tant que plugin
  .use(router)
  .use(store)
  .mount("#app")
