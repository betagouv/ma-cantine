import { createApp } from "vue"
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque

// Vuetify
import "vuetify/styles"
import { createVuetify } from "vuetify"
import * as components from "vuetify/components"
import * as directives from "vuetify/directives"

const vuetify = createVuetify({
  components,
  directives,
})

import App from "./App.vue"
import { router } from "./router"
import store from "./store"

createApp(App)
  .use(vuetify)
  .use(VueDsfr) // Enregistrement de la bibliothèque en tant que plugin
  .use(router)
  .use(store)
  .mount("#app")
