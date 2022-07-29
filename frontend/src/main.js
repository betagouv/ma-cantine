import Vue from "vue"
import VueMatomo from "vue-matomo"
import App from "./App.vue"
import { router } from "./router"
import store from "./store"
import vuetify from "./plugins/vuetify"

Vue.config.productionTip = false

if (window.MATOMO_ID) {
  Vue.use(VueMatomo, {
    host: "https://stats.data.gouv.fr",
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

new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount("#app")
