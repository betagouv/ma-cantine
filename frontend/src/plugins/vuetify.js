import "vuetify/styles"
import { createVuetify } from "vuetify"
import maCantineTheme from "@/theme"
import { VBtn, VCard, VRadio, VCheckbox } from "vuetify/components"
import remixJson from "./remix.json"

// Defaults to conform to DSFR
VBtn.props.ripple.default = false
VBtn.props.elevation.default = 0
VCard.props.ripple.default = false
VRadio.props.ripple.default = false
VCheckbox.props.ripple.default = false

export default createVuetify({
  theme: {
    defaultTheme: "maCantineTheme",
    themes: {
      maCantineTheme,
    },
  },
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
    aliases: remixJson,
  },
})
