import Vue from "vue"
import Vuetify from "vuetify/lib/framework"
import theme from "@/theme"
import { VBtn, VCard } from "vuetify/lib"
import remixJson from "./remix.json"

Vue.use(Vuetify)

// Defaults to conform to DSFR
VBtn.options.props.ripple.default = false
VBtn.options.props.elevation.default = 0
VCard.options.props.ripple.default = false

export default new Vuetify({
  theme: theme,
  iconfont: "md",
  breakpoint: {
    mobileBreakpoint: "sm",
  },
  /*
  remixJson contains a key-value pair of icon names and svg paths. These correspond to the icons
  on https://www.systeme-de-design.gouv.fr/elements-d-interface/fondamentaux-techniques/icones.
  To use them, instead of using the "mdi-" prefix, just append a dollar sign. For example, to use
  icon "cloudy-2-fill" you can use "<v-icon>$cloudy-2-fill</v-icon>".

  Note that not all Remix icons are included, only those chosen by the DSFR. MDI icons are still
  available.
  */
  icons: {
    iconfont: "mdi",
    values: remixJson,
  },
})
