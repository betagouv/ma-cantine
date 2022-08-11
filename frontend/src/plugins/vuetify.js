import Vue from "vue"
import Vuetify from "vuetify/lib/framework"
import theme from "@/theme"
import { VBtn, VCard } from "vuetify/lib"

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
})
