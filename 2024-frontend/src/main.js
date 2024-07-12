import "./assets/main.css"

import { createApp } from "vue"
import { createPinia } from "pinia"
import "@gouvfr/dsfr/dist/core/core.main.min.css" // Le CSS minimal du DSFR
import "@gouvfr/dsfr/dist/component/component.main.min.css" // Styles de tous les composants du DSFR
import "@gouvfr/dsfr/dist/utility/utility.main.min.css" // Classes utilitaires : les composants de VueDsfr en ont besoin
import "@gouvminint/vue-dsfr/styles" // Les styles propres aux composants de VueDsfr
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque

import App from "./App.vue"
import router from "./router"

const app = createApp(App)

app.use(VueDsfr)
app.use(createPinia())
app.use(router)

app.mount("#app")
